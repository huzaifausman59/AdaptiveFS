function greet(name) {
    const message = `Hello, ${name}!`;
    console.log(message);
    return message;
}

document.addEventListener("DOMContentLoaded", () => {
    window.onload = () => greet("World");
});

module.exports = { greet };
