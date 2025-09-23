const showOverlayMenu = () => {
    document.body.classList.remove("menu-hide");
    document.body.classList.add("menu-open");
    document.getElementsByClassName("sidenav-overlay")[0].classList.add("show");
};

const hideOverlayMenu = () => {
    document.body.classList.add("menu-hide");
    document.body.classList.remove("menu-open");
    document.getElementsByClassName("sidenav-overlay")[0].classList.remove("show");
};

const showStaticMenu = () => {
    document.body.classList.add("menu-expanded", "vertical-menu-modern");
    document.body.classList.remove("vertical-overlay-menu");
};

const hideStaticMenu = () => {
    document.body.classList.remove("menu-expanded", "vertical-menu-modern");
    document.body.classList.add("vertical-overlay-menu");
};

export {
    showOverlayMenu,
    hideOverlayMenu,
    showStaticMenu,
    hideStaticMenu
}