export function outsideClick(node: HTMLElement) {
    window.addEventListener('click', handleClick);

    function handleClick(e: MouseEvent) {
        if (!node.contains(e.target as Node)) {
            node.dispatchEvent(new CustomEvent('outsideclick'))
        }
    }

    return {
        destroy() {
            window.removeEventListener('click', handleClick)
        }
    };
}