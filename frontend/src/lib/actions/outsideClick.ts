export function outsideClick(node: HTMLElement, options?: { ignore?: string }) {
    const ignoreSelector = options?.ignore ?? '';

    function handleClick(e: MouseEvent) {
        const target = e.target as HTMLElement;
        if (node.contains(target)) return;
        if (ignoreSelector && target.closest(ignoreSelector)) return;
        node.dispatchEvent(new CustomEvent('outsideclick'));
    }

    document.addEventListener('pointerdown', handleClick);

    return {
        destroy() {
            document.removeEventListener('pointerdown', handleClick);
        }
    };
}