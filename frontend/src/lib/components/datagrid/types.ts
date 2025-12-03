export interface ColumnHeaderProps {
    sort: boolean;
    title: string;
    sortName?: "created_at" | "transaction_fee" | "transaction_status";
    order?: "asc" | "desc";
    onClick?: (name: "created_at" | "transaction_fee" | "transaction_status") => void;
}