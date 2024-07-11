document.addEventListener("DOMContentLoaded", function() {
    gsap.from(".container", { duration: 1, opacity: 0, y: -50 });
    gsap.from("h1", { duration: 1, opacity: 0, x: -100, delay: 0.5 });
    gsap.from("h3", { duration: 1, opacity: 0, x: 100, delay: 1 });
    gsap.from("form", { duration: 1, opacity: 0, scale: 0.8, delay: 1.5 });

    const button = document.querySelector("button");
    button.addEventListener("click", function() {
        gsap.to(button, { duration: 0.3, scale: 0.9, yoyo: true, repeat: 1 });
    });

    if (document.querySelector(".handwritten-image")) {
        gsap.from(".handwritten-image", { duration: 1, opacity: 0, scale: 0.5, delay: 2 });
    }
});
