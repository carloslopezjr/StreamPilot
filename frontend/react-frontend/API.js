export default class API {
    
    static async scheduleStream(payload) {
        const response = await fetch("http://localhost:8080/schedule_stream", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        if (response.status === 401) {
            // Not authenticated — get auth_url and redirect
            const data = await response.json();
            if (data.auth_required && data.auth_url) {
            window.location.href = data.auth_url;
            return;
            }
        }

        if (response.ok) {
            const data = await response.json();
            console.log(data.message);
            return data;
        } else {
            console.error("Failed to schedule stream:", response.status);
        }
    }
}