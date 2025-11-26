// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
    namespace App {
        // interface Error {}
        // interface Locals {}
        // interface PageData {}
        // interface PageMenuState {}
        // interface Platform {}
    }

    declare namespace svelteHTML {
        interface HTMLAttributes<T> {
            'on:outsideclick'?: (event: CustomEvent<void>) => void;
        }
    }
}

export {};
