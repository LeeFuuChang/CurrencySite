requirejs.config({
    //By default load any module IDs from js/lib
    baseUrl: "assets/js",
    paths: {
        contents: "../js/contents"
    }
});

// Start the main app logic.
requirejs(["header", "footer", "login", "content", "contents/content_type1"],
function   (header, footer, content, content_type1){});