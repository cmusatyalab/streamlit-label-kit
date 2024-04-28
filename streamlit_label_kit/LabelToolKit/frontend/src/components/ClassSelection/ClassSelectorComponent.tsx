export type ClassSelectorProps<Multiple extends boolean> = {
  label_list: string[];
  label: SelectValue<Multiple>;
  multi?: Multiple;
}

export type SelectValue<Multiple> = Multiple extends true ? string[] : string;
