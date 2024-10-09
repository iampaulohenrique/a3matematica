async function sendMessage(userId, key, message, mediaType) {
    const response = await fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userId, key, message, media_type: mediaType }),
    });

    const result = await response.json();
    console.log(result);
}
