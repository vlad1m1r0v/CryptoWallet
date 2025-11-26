import type { Component } from 'svelte';


export default interface MenuItemProps {
    checkIsActive: (currentUrl: URL) => boolean;
    canBeShown?: boolean;
    Icon: Component;
    title: string;
    href: string;
}