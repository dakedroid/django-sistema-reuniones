/**
 * Gráfica en forma de flor para visualizar capacitaciones por categoría formativa y curso específico
 * Inspirada en el diagrama de marketing online
 */

class GraficaFlor {
    constructor(containerId, data) {
        this.container = d3.select(`#${containerId}`);
        this.data = data;
        this.width = 900;
        this.height = 700;
        this.radius = Math.min(this.width, this.height) / 2 - 100;
        
        // Colores para cada categoría (pétalos)
        this.colores = [
            '#4A90E2', // Azul
            '#7ED321', // Verde  
            '#F5A623', // Amarillo
            '#D0021B', // Rojo
            '#9013FE', // Púrpura
            '#50E3C2', // Turquesa
            '#BD10E0', // Magenta
            '#B8E986', // Verde claro
        ];
        
        this.init();
    }
    
    init() {
        // Limpiar container existente
        this.container.selectAll("*").remove();
        
        // Crear SVG centrado con estilo
        this.svg = this.container.append("svg")
            .attr("width", this.width)
            .attr("height", this.height)
            .style("display", "block")
            .style("margin", "0 auto");
            
        // Grupo principal centrado en el SVG
        this.g = this.svg.append("g")
            .attr("transform", `translate(${this.width/2},${this.height/2})`);
            
        this.crearLeyenda();
        this.crearFlor();
        this.crearTooltips();
    }
    
    crearFlor() {
        // Calcular ángulos para cada pétalo
        const numPetalos = this.data.categorias.length;
        const angleStep = (2 * Math.PI) / numPetalos;
        
        // Crear pétalos
        this.data.categorias.forEach((categoria, index) => {
            const angle = index * angleStep;
            const color = this.colores[index % this.colores.length];
            
            this.crearPetalo(categoria, angle, color, index);
        });
        
        // Crear centro de la flor
        this.crearCentro();
    }
    
    crearPetalo(categoria, angle, color, index) {
        const numPetalos = this.data.categorias.length;
        
        // Ajustar tamaño según número de pétalos para evitar solapamiento
        const factorEscala = Math.max(0.6, 1 - (numPetalos - 3) * 0.08);
        const petalRadius = this.radius * 0.85 * factorEscala;
        const petalWidth = this.radius * 0.50 * factorEscala;
        
        // Calcular posición del pétalo (más separado del centro)
        const distanciaDelCentro = petalRadius * 0.65;
        const x = Math.cos(angle - Math.PI/2) * distanciaDelCentro;
        const y = Math.sin(angle - Math.PI/2) * distanciaDelCentro;
        
        // Crear grupo para el pétalo
        const petalGroup = this.g.append("g")
            .attr("class", `petalo petalo-${index}`)
            .attr("transform", `translate(${x},${y}) rotate(${angle * 180/Math.PI})`);
        
        // Crear forma del pétalo tipo trébol (más redondeado)
        const petalo = petalGroup.append("ellipse")
            .attr("rx", petalWidth)
            .attr("ry", petalRadius)
            .attr("fill", color)
            .attr("fill-opacity", 0.85)
            .attr("stroke", "#ffffff")
            .attr("stroke-width", 3)
            .style("filter", "drop-shadow(0px 2px 4px rgba(0,0,0,0.2))");
        
        // Ajustar tamaño de fuente según número de pétalos
        const fontSize = Math.max(10, 14 - numPetalos * 0.5);
        const fontSizeNumero = Math.max(12, 18 - numPetalos * 0.6);
        
        // Agregar texto del pétalo
        const texto = petalGroup.append("text")
            .attr("text-anchor", "middle")
            .attr("dy", "-0.5em")
            .attr("fill", "white")
            .attr("font-weight", "bold")
            .attr("font-size", `${fontSize}px`)
            .style("pointer-events", "none");
            
        // Dividir texto en líneas para mejor legibilidad
        const palabras = categoria.nombre.split(' ');
        const maxPalabrasPorLinea = 2;
        
        if (palabras.length > maxPalabrasPorLinea) {
            // Primera línea
            texto.append("tspan")
                .attr("x", 0)
                .attr("dy", "0em")
                .text(palabras.slice(0, maxPalabrasPorLinea).join(' '));
            // Segunda línea
            texto.append("tspan")
                .attr("x", 0)
                .attr("dy", "1.2em")
                .text(palabras.slice(maxPalabrasPorLinea).join(' '));
        } else if (palabras.length === 2) {
            texto.append("tspan")
                .attr("x", 0)
                .attr("dy", "0em")
                .text(palabras[0]);
            texto.append("tspan")
                .attr("x", 0)
                .attr("dy", "1.2em")
                .text(palabras[1]);
        } else {
            texto.text(categoria.nombre);
        }
        
        // Agregar número de capacitados (más grande y destacado)
        petalGroup.append("text")
            .attr("text-anchor", "middle")
            .attr("dy", `${palabras.length > 1 ? 3.2 : 2.0}em`)
            .attr("fill", "white")
            .attr("font-weight", "bold")
            .attr("font-size", `${fontSizeNumero}px`)
            .style("pointer-events", "none")
            .style("text-shadow", "0px 1px 2px rgba(0,0,0,0.5)")
            .text(categoria.total);
        
        // Hacer el grupo completo interactivo
        petalGroup.style("cursor", "pointer");
        
        // Variable para guardar referencia al contexto y transformación original
        const self = this;
        const transformOriginal = `translate(${x},${y}) rotate(${angle * 180/Math.PI})`;
        const transformHover = `translate(${x},${y}) rotate(${angle * 180/Math.PI}) scale(1.15)`;
        
        // Efectos de hover
        petalGroup
            .on("mouseover", function() {
                // Traer el pétalo al frente - mover al final del DOM (SE QUEDA AL FRENTE)
                const currentGroup = this;
                currentGroup.parentNode.appendChild(currentGroup);
                
                // Escalar el pétalo (la elipse)
                petalo.transition()
                    .duration(200)
                    .attr("fill-opacity", 1);
                
                // Escalar todo el grupo SIN mover la posición
                d3.select(currentGroup)
                    .transition()
                    .duration(200)
                    .attr("transform", transformHover);
                    
                self.mostrarTooltip(categoria, index);
            })
            .on("mouseout", function() {
                // NO movemos el pétalo de vuelta, se queda al frente
                
                petalo.transition()
                    .duration(200)
                    .attr("fill-opacity", 0.85);
                
                // Volver al tamaño original PERO mantener la posición
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr("transform", transformOriginal);
                    
                self.ocultarTooltip();
            })
            .on("click", function() {
                self.expandirPetalo(categoria, index);
            });
    }
    
    crearCentro() {
        // Círculo central más grande y con sombra
        this.g.append("circle")
            .attr("r", 70)
            .attr("fill", "#2C3E50")
            .attr("stroke", "#ffffff")
            .attr("stroke-width", 5)
            .style("filter", "drop-shadow(0px 3px 6px rgba(0,0,0,0.3))");
        
        // Texto central
        this.g.append("text")
            .attr("text-anchor", "middle")
            .attr("dy", "-0.8em")
            .attr("fill", "white")
            .attr("font-weight", "bold")
            .attr("font-size", "13px")
            .attr("letter-spacing", "1px")
            .text("CAPACITACIONES");
            
        this.g.append("text")
            .attr("text-anchor", "middle")
            .attr("dy", "0.8em")
            .attr("fill", "white")
            .attr("font-weight", "bold")
            .attr("font-size", "24px")
            .style("text-shadow", "0px 2px 4px rgba(0,0,0,0.5)")
            .text(this.data.total);
            
        this.g.append("text")
            .attr("text-anchor", "middle")
            .attr("dy", "2.3em")
            .attr("fill", "#BDC3C7")
            .attr("font-size", "11px")
            .attr("letter-spacing", "0.5px")
            .text("TOTAL");
    }
    
    crearLeyenda() {
        // Leyenda en la parte superior izquierda (como estaba originalmente)
        const leyenda = this.svg.append("g")
            .attr("class", "leyenda")
            .attr("transform", "translate(20, 20)");
            
        leyenda.append("text")
            .attr("x", 0)
            .attr("y", 0)
            .attr("font-weight", "bold")
            .attr("font-size", "16px")
            .attr("fill", "#2C3E50")
            .text("Categorías Formativas");
            
        // Ítems de leyenda en vertical
        this.data.categorias.forEach((categoria, index) => {
            const item = leyenda.append("g")
                .attr("transform", `translate(0, ${30 + index * 25})`);
                
            item.append("circle")
                .attr("r", 8)
                .attr("fill", this.colores[index % this.colores.length]);
                
            item.append("text")
                .attr("x", 20)
                .attr("y", 5)
                .attr("font-size", "12px")
                .attr("fill", "#2C3E50")
                .text(`${categoria.nombre} (${categoria.total})`);
        });
    }
    
    crearTooltips() {
        this.tooltip = d3.select("body").append("div")
            .attr("class", "tooltip-flor")
            .style("opacity", 0)
            .style("position", "absolute")
            .style("background", "rgba(0, 0, 0, 0.8)")
            .style("color", "white")
            .style("padding", "10px")
            .style("border-radius", "5px")
            .style("pointer-events", "none")
            .style("font-size", "12px");
    }
    
    mostrarTooltip(categoria, index) {
        let html = `
            <strong>${categoria.nombre}</strong><br>
            <strong>Total capacitados:</strong> ${categoria.total}<br><br>
            <strong>Cursos específicos:</strong><br>
        `;
        
        categoria.cursos.forEach(curso => {
            html += `• ${curso.nombre}: ${curso.total}<br>`;
        });
        
        this.tooltip
            .style("opacity", 1)
            .html(html)
            .style("left", (d3.event.pageX + 10) + "px")
            .style("top", (d3.event.pageY - 10) + "px");
    }
    
    ocultarTooltip() {
        this.tooltip.style("opacity", 0);
    }
    
    expandirPetalo(categoria, index) {
        // Crear vista expandida de cursos específicos
        this.mostrarDetallesCursos(categoria);
    }
    
    mostrarDetallesCursos(categoria) {
        // Modal o panel lateral con detalles de cursos
        const modal = d3.select("body").append("div")
            .attr("class", "modal-cursos")
            .style("position", "fixed")
            .style("top", "0")
            .style("left", "0")
            .style("width", "100%")
            .style("height", "100%")
            .style("background", "rgba(0, 0, 0, 0.5)")
            .style("z-index", "1000")
            .on("click", function() {
                d3.select(this).remove();
            });
            
        const contenido = modal.append("div")
            .style("position", "absolute")
            .style("top", "50%")
            .style("left", "50%")
            .style("transform", "translate(-50%, -50%)")
            .style("background", "white")
            .style("padding", "20px")
            .style("border-radius", "10px")
            .style("max-width", "500px")
            .style("max-height", "70%")
            .style("overflow-y", "auto")
            .on("click", function() {
                d3.event.stopPropagation();
            });
            
        contenido.append("h3")
            .style("margin-top", "0")
            .style("color", "#2C3E50")
            .text(categoria.nombre);
            
        contenido.append("p")
            .text(`Total de capacitados: ${categoria.total}`);
            
        const lista = contenido.append("ul");
        categoria.cursos.forEach(curso => {
            lista.append("li")
                .html(`<strong>${curso.nombre}:</strong> ${curso.total} capacitados`);
        });
        
        contenido.append("button")
            .style("margin-top", "20px")
            .style("padding", "10px 20px")
            .style("background", "#3498DB")
            .style("color", "white")
            .style("border", "none")
            .style("border-radius", "5px")
            .style("cursor", "pointer")
            .text("Cerrar")
            .on("click", function() {
                modal.remove();
            });
    }
    
    // Método para actualizar datos
    actualizarDatos(nuevosDatos) {
        this.data = nuevosDatos;
        this.init();
    }
}

// Función para cargar datos desde el servidor
async function cargarDatosCapacitacion() {
    try {
        const response = await fetch('/api/estadisticas-capacitacion/');
        const data = await response.json();
        console.log('Datos recibidos:', data); // Debug
        return data;
    } catch (error) {
        console.error('Error cargando datos:', error);
        // Datos de ejemplo para testing
        return {
            total: 150,
            categorias: [
                {
                    codigo: 'DOCENTE',
                    nombre: 'Docente',
                    total: 85,
                    cursos: [
                        { codigo: 'CIENCIA_DATOS', nombre: 'Ciencia de Datos', total: 25 },
                        { codigo: 'INTELIGENCIA_ARTIFICIAL', nombre: 'Inteligencia Artificial', total: 30 },
                        { codigo: 'METODOLOGIA_INVESTIGACION', nombre: 'Metodología de Investigación', total: 30 }
                    ]
                },
                {
                    codigo: 'ADMINISTRATIVO',
                    nombre: 'Administrativo',
                    total: 35,
                    cursos: [
                        { codigo: 'LIDERAZGO', nombre: 'Liderazgo', total: 20 },
                        { codigo: 'GESTION_PROYECTOS', nombre: 'Gestión de Proyectos', total: 15 }
                    ]
                },
                {
                    codigo: 'DIRECTIVO',
                    nombre: 'Directivo',
                    total: 30,
                    cursos: [
                        { codigo: 'PLANEACION_ESTRATEGICA', nombre: 'Planeación Estratégica', total: 15 },
                        { codigo: 'CALIDAD_EDUCATIVA', nombre: 'Calidad Educativa', total: 15 }
                    ]
                }
            ]
        };
    }
}

// Función para verificar si D3 está disponible
function checkD3Availability() {
    return new Promise((resolve, reject) => {
        if (typeof d3 !== 'undefined') {
            resolve(true);
        } else {
            // Esperar un poco más y volver a verificar
            let attempts = 0;
            const maxAttempts = 10;
            const checkInterval = setInterval(() => {
                attempts++;
                if (typeof d3 !== 'undefined') {
                    clearInterval(checkInterval);
                    resolve(true);
                } else if (attempts >= maxAttempts) {
                    clearInterval(checkInterval);
                    reject(new Error('D3.js no se pudo cargar después de varios intentos'));
                }
            }, 100);
        }
    });
}

// Inicializar gráfica cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', async function() {
    console.log('DOM cargado, buscando contenedor...'); // Debug
    
    const contenedor = document.getElementById('grafica-flor-capacitaciones');
    if (contenedor) {
        console.log('Contenedor encontrado, verificando D3 y datos...'); // Debug
        
        try {
            // Verificar que D3 esté disponible
            await checkD3Availability();
            console.log('D3.js disponible, versión:', d3.version); // Debug
            
            // Usar datos del contexto de Django si están disponibles
            let datos;
            if (window.datosCapacitacion) {
                datos = window.datosCapacitacion;
                console.log('Usando datos del contexto Django:', datos); // Debug
            } else {
                console.log('No hay datos en contexto, usando datos de ejemplo...'); // Debug
                // Datos de ejemplo si no hay datos del servidor
                datos = {
                    total: 245,
                    categorias: [
                        {
                            codigo: 'DOCENTE',
                            nombre: 'Docente',
                            total: 120,
                            cursos: [
                                { codigo: 'CIENCIA_DATOS', nombre: 'Ciencia de Datos', total: 45 },
                                { codigo: 'INTELIGENCIA_ARTIFICIAL', nombre: 'Inteligencia Artificial', total: 35 },
                                { codigo: 'METODOLOGIA_INVESTIGACION', nombre: 'Metodología de Investigación', total: 40 }
                            ]
                        },
                        {
                            codigo: 'ADMINISTRATIVO',
                            nombre: 'Administrativo',
                            total: 65,
                            cursos: [
                                { codigo: 'LIDERAZGO', nombre: 'Liderazgo', total: 30 },
                                { codigo: 'GESTION_PROYECTOS', nombre: 'Gestión de Proyectos', total: 20 },
                                { codigo: 'RECURSOS_HUMANOS', nombre: 'Gestión de Recursos Humanos', total: 15 }
                            ]
                        },
                        {
                            codigo: 'DIRECTIVO',
                            nombre: 'Directivo',
                            total: 35,
                            cursos: [
                                { codigo: 'PLANEACION_ESTRATEGICA', nombre: 'Planeación Estratégica', total: 20 },
                                { codigo: 'CALIDAD_EDUCATIVA', nombre: 'Calidad Educativa', total: 15 }
                            ]
                        },
                        {
                            codigo: 'INVESTIGADOR',
                            nombre: 'Investigador',
                            total: 25,
                            cursos: [
                                { codigo: 'REDACCION_CIENTIFICA', nombre: 'Redacción Científica', total: 15 },
                                { codigo: 'ESTADISTICA_AVANZADA', nombre: 'Estadística Avanzada', total: 10 }
                            ]
                        }
                    ]
                };
            }
            
            console.log('Creando gráfica con datos:', datos); // Debug
            const grafica = new GraficaFlor('grafica-flor-capacitaciones', datos);
            
            // Guardar referencia global para poder actualizar
            window.graficaCapacitaciones = grafica;
            
            console.log('Gráfica creada exitosamente'); // Debug
        } catch (error) {
            console.error('Error creando gráfica:', error);
            
            // Mostrar mensaje de error en el contenedor
            contenedor.innerHTML = `
                <div class="alert alert-warning text-center">
                    <i class="fas fa-exclamation-triangle fa-2x mb-3"></i>
                    <h5>Error cargando la gráfica</h5>
                    <p>Error: ${error.message}</p>
                    <button class="btn btn-primary" onclick="location.reload()">Recargar</button>
                </div>
            `;
        }
    } else {
        console.error('Contenedor grafica-flor-capacitaciones no encontrado'); // Debug
    }
});