function formatTime(dateString) {
    // If we have actual date data
    if (dateString) {
        const date = new Date(dateString);
        return date.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' });
    }
    // Otherwise return placeholder
    return 'Hace poco';
}

function getStatusColor(status) {
    switch(status) {
        case 'completed':
            return 'bg-green-100 text-green-800';
        case 'pending':
            return 'bg-yellow-100 text-yellow-800';
        case 'canceled':
            return 'bg-red-100 text-red-800';
        default:
            return 'bg-gray-100 text-gray-800';
    }
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}


