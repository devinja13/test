import { getCoreRowModel, useReactTable } from "@tanstack/react-table";
import { ColumnDef } from "@tanstack/react-table"; // Make sure you've imported this
import { DataTable } from "./ui/DataTable";

// types import
import { ScheduleItem } from "../types/schedule";

type ScheduleTableProps = {
  schedule: ScheduleItem[];
};
type GroupedSchedule = {
  fullName: string;
  items: ScheduleItem[];
  shiftsCount: number;
  shifts: string;
  availability: string[];
  role: string;
  oc_status: string;
};

function groupByFullName(scheduleItems: ScheduleItem[]) {
  // Create a map to store shifts by person
  const personMap = new Map<string, ScheduleItem[]>();

  scheduleItems.forEach((item) => {
    const fullName = `${item.first_name} ${item.last_name}`;

    if (!personMap.has(fullName)) {
      personMap.set(fullName, []);
    }

    personMap.get(fullName)!.push(item);
  });

  // Convert map to array format
  return Array.from(personMap.entries()).map(([fullName, items]) => ({
    fullName,
    items,
    shiftsCount: items.length,
    shifts: items.map((item) => item.shift).join(", "),
    availability: items[0].availability,
    role: items[0].role,
    oc_status: items[0].oc_status ? "Yes" : "No",
  }));
}

// column definitions for the columns
const columns: ColumnDef<GroupedSchedule, any>[] = [
  {
    accessorKey: "fullName", // key of the row object used to extract the value for a column
    header: "Name",
    cell: (props: any) => <p>{props.getValue()}</p>, // custom react component taht we actually render
  },
  {
    accessorKey: "shiftsCount",
    header: "Number of Shifts",
    cell: (props: any) => <p>{props.getValue()}</p>,
  },
  {
    accessorKey: "shifts",
    header: "Shifts",
    cell: (props: any) => <p>{props.getValue()}</p>,
  },
  {
    accessorKey: "availability",
    header: "Availability",
    cell: (props: any) => <p>{props.getValue()}</p>,
  },
  {
    accessorKey: "role",
    header: "Role",
    cell: (props: any) => <p>{props.getValue()}</p>,
  },
  {
    accessorKey: "oc_status",
    header: "Off Campus?",
    cell: (props: any) => <p>{props.getValue()}</p>,
  },
];

export default function ScheduleTable({ schedule }: ScheduleTableProps) {
  // grouping our shift schedule items by name
  const groupedScheduleByPerson = groupByFullName(schedule);

  const table = useReactTable({
    data: groupedScheduleByPerson,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return <DataTable columns={columns} data={groupedScheduleByPerson} />;
}
