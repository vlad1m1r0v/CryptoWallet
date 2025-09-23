export function openModal(modal: HTMLDivElement) {
    modal.style.display = 'block';
    modal.classList.add('fade');

    const backdrop = document.createElement('div');
    backdrop.className = 'modal-backdrop fade';
    document.body.appendChild(backdrop);

    requestAnimationFrame(() => {
        modal.classList.add('show');
        backdrop.classList.add('show');
    });

    document.body.classList.add('modal-open');
}

export function closeModal(modal: HTMLDivElement) {
    modal.classList.remove('show');
    const backdrop = document.querySelector('.modal-backdrop');

    if (backdrop) {
        backdrop.classList.remove('show');
    }

    setTimeout(() => {
        modal.style.display = 'none';
        document.body.classList.remove('modal-open');
        if (backdrop) backdrop.remove();
    }, 300);
}