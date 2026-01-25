async function fetchEvents() {
    try {
        const res = await fetch("/events");
        const events = await res.json();

        const container = document.getElementById("events");
        container.innerHTML = "";

        events.forEach(event => {
            const div = document.createElement("div");
            div.className = "event";

            let text = "";

            const date = new Date(event.timestamp).toUTCString();

            if (event.action === "PUSH") {
                text = `${event.author} pushed to ${event.to_branch} on ${date}`;
            }

            if (event.action === "PULL_REQUEST") {
                text = `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${date}`;
            }

            if (event.action === "MERGE") {
                text = `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${date}`;
            }

            div.innerText = text;
            container.appendChild(div);
        });

    } catch (err) {
        console.error("Failed to fetch events", err);
    }
}

// initial load
fetchEvents();

// poll every 15 seconds
setInterval(fetchEvents, 15000);
