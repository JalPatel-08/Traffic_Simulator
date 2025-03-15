function fetchTrafficData() {
    fetch('/traffic')
        .then(response => response.json())
        .then(data => {
            document.getElementById("junction_id").textContent = data.junction_id || "-";
            document.getElementById("vehicle_count").textContent = data.vehicle_count || "-";
            document.getElementById("avg_speed").textContent = data.avg_speed || "-";
            document.getElementById("congestion").textContent = data.congestion || "-";
            document.getElementById("signal_duration").textContent = data.signal_duration || "-";
        })
        .catch(error => console.error("Error fetching data:", error));
}

// Refresh data every 2 seconds
setInterval(fetchTrafficData, 2000);
fetchTrafficData();
