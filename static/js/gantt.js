// gantt.js - Handles Gantt chart visualization

// Wait for DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Gantt chart if the container exists
    if (document.getElementById('actividadesGantt')) {
        initGanttChart();
    }
});

// Initialize Gantt Chart
function initGanttChart() {
    // Get the Gantt container and data
    const ganttContainer = document.getElementById('actividadesGantt');
    const actividadesData = JSON.parse(ganttContainer.getAttribute('data-actividades'));
    
    // Define date range for the gantt chart
    let minDate = new Date('2023-01-01');
    let maxDate = new Date('2023-12-31');
    
    // Find the actual min/max dates from the data if available
    if (actividadesData && actividadesData.length > 0) {
        const startDates = actividadesData.map(a => new Date(a.inicio));
        const endDates = actividadesData.map(a => new Date(a.fin));
        
        minDate = new Date(Math.min(...startDates));
        maxDate = new Date(Math.max(...endDates));
        
        // Add some padding to the date range
        minDate.setMonth(minDate.getMonth() - 1);
        maxDate.setMonth(maxDate.getMonth() + 1);
    }
    
    // Calculate total days in the range for positioning
    const totalDays = (maxDate - minDate) / (1000 * 60 * 60 * 24);
    
    // Create the timeline header
    createTimelineHeader(ganttContainer, minDate, maxDate);
    
    // Create gantt rows for each activity
    actividadesData.forEach(actividad => {
        createGanttRow(ganttContainer, actividad, minDate, totalDays);
    });
}

// Create the timeline header with months
function createTimelineHeader(container, startDate, endDate) {
    // Create timeline container
    const timeline = document.createElement('div');
    timeline.className = 'gantt-timeline';
    
    // Create month labels
    const months = [];
    const currentDate = new Date(startDate);
    
    while (currentDate <= endDate) {
        months.push(new Date(currentDate));
        currentDate.setMonth(currentDate.getMonth() + 1);
    }
    
    // Add month cells
    months.forEach(month => {
        const monthCell = document.createElement('div');
        monthCell.className = 'gantt-month';
        monthCell.textContent = month.toLocaleDateString('es-MX', { month: 'short', year: 'numeric' });
        timeline.appendChild(monthCell);
    });
    
    container.appendChild(timeline);
}

// Create a gantt row for an activity
function createGanttRow(container, activity, minDate, totalDays) {
    // Create row container
    const row = document.createElement('div');
    row.className = 'gantt-row';
    
    // Create label
    const label = document.createElement('div');
    label.className = 'gantt-row-label';
    label.textContent = activity.actividad;
    row.appendChild(label);
    
    // Create bars container
    const barsContainer = document.createElement('div');
    barsContainer.className = 'gantt-row-bars';
    
    // Calculate position and width of the activity bar
    const startDate = new Date(activity.inicio);
    const endDate = new Date(activity.fin);
    
    const startDays = (startDate - minDate) / (1000 * 60 * 60 * 24);
    const durationDays = (endDate - startDate) / (1000 * 60 * 60 * 24);
    
    const startPercent = (startDays / totalDays) * 100;
    const widthPercent = (durationDays / totalDays) * 100;
    
    // Create activity bar
    const bar = document.createElement('div');
    bar.className = 'gantt-bar';
    bar.style.left = `${startPercent}%`;
    bar.style.width = `${widthPercent}%`;
    
    // Assign a different color based on the activity ID (for variety)
    const colors = [
        'rgba(52, 152, 219, 0.8)',   // Blue
        'rgba(155, 89, 182, 0.8)',    // Purple
        'rgba(46, 204, 113, 0.8)',    // Green
        'rgba(230, 126, 34, 0.8)',    // Orange
        'rgba(231, 76, 60, 0.8)',     // Red
        'rgba(241, 196, 15, 0.8)',    // Yellow
        'rgba(26, 188, 156, 0.8)',    // Turquoise
        'rgba(52, 73, 94, 0.8)'       // Dark Blue
    ];
    
    const colorIndex = (activity.id - 1) % colors.length;
    bar.style.backgroundColor = colors[colorIndex];
    
    // Add label inside the bar if there's enough space
    const label2 = document.createElement('div');
    label2.className = 'gantt-bar-label';
    
    // Format dates
    const formattedStart = startDate.toLocaleDateString('es-MX', { day: '2-digit', month: 'short' });
    const formattedEnd = endDate.toLocaleDateString('es-MX', { day: '2-digit', month: 'short' });
    
    // Only show dates if the bar is wide enough
    if (widthPercent > 10) {
        label2.textContent = `${formattedStart} - ${formattedEnd}`;
    }
    
    bar.appendChild(label2);
    barsContainer.appendChild(bar);
    row.appendChild(barsContainer);
    
    // Add tooltip
    bar.title = `${activity.actividad}: ${formattedStart} - ${formattedEnd}`;
    
    container.appendChild(row);
}
