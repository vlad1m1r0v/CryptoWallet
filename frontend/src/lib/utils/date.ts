export function formatDate(dateStr: string | null | undefined): string {
        if (!dateStr) return '';

        const date = new Date(dateStr);

        return new Intl.DateTimeFormat('uk-UA', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            timeZone: 'Europe/Kyiv'
        }).format(date).replace(',', '');
    }