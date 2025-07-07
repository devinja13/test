import { useLocation } from "react-router-dom";
import { useState, useRef, useEffect } from "react";

// Full Calendar Elements
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";

// component import
import ScheduleTable from "./ScheduleTable";
import ExportToCalendarButton from "./ExportToCalendarButton";
//types imports
import { ScheduleItem } from "../types/schedule";
// util for calendar event dates
import parseDateString from "../util/DateParser";
// unique ids for calendar changes and getting events by id
import { v4 as uuidv4 } from "uuid";
import { DateTime } from "luxon";
import { EventDropArg } from "@fullcalendar/core/index.js";

export default function GeneratedSchedule() {
  const location = useLocation();
  const initializedSchedule: ScheduleItem[] = location.state.schedule.map(
    (item: Omit<ScheduleItem, "id">) => ({
      ...item,
      id: uuidv4(),
    })
  );
  // console.log(initializedSchedule);
  const [schedule, setSchedule] = useState<ScheduleItem[]>(initializedSchedule);

  const mouseY = useRef(0);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      mouseY.current = e.clientY;
    };
    document.addEventListener("mousemove", handleMouseMove);
    return () => {
      document.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  // // makes sure that events can only be placed on 8AM or 8PM
  const handleEventDrop = (info: EventDropArg) => {
    const droppedDate = info.event.start!; // real drop target
    let hour = 8;

    if (info.view.type === "dayGridMonth") {
      // Use mouse Y coordinate to determine top/bottom of the target day cell
      const pointY = info.jsEvent.clientY;

      // Find all day cells on the screen
      const dayEls = document.querySelectorAll(".fc-daygrid-day");
      dayEls.forEach((cell) => {
        const bounds = cell.getBoundingClientRect();

        if (
          pointY >= bounds.top &&
          pointY <= bounds.bottom &&
          info.jsEvent.clientX >= bounds.left &&
          info.jsEvent.clientX <= bounds.right
        ) {
          const midpoint = bounds.top + bounds.height / 2;
          if (pointY > midpoint) {
            hour = 20;
          }
        }
      });
    } else {
      hour = droppedDate.getHours() < 14 ? 8 : 20;
    }

    const coerced = DateTime.fromJSDate(droppedDate).set({
      hour,
      minute: 0,
      second: 0,
      millisecond: 0,
    });

    const newShift = coerced.toFormat("ccc, LLLL d, ha"); // same format parser expects

    setSchedule((prev) =>
      prev.map((assignment) =>
        assignment.id === info.event.id
          ? { ...assignment, shift: newShift }
          : assignment
      )
    );
  };

  return (
    <>
      <div className="flex align-middle justify-center">
        <ExportToCalendarButton schedule={schedule} />
      </div>
      <div className="mt-2 mx-2 px-4 py-4 flex gap-5">
        <div className="flex-1 max-w-3/5 max-h-">
          <FullCalendar
            height="100%"
            plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
            initialView="timeGridWeek"
            editable={true}
            slotDuration="01:00:00"
            slotLabelInterval={{ hours: 4 }}
            headerToolbar={{
              start: "today prev,next",
              center: "title",
              end: "dayGridMonth,timeGridWeek,timeGridDay",
            }}
            // Renders shifts onto screen with date parsing
            events={schedule.map((item) => {
              const parsedDate: Date = parseDateString(item.shift);
              const endDate = new Date(parsedDate);
              endDate.setHours(endDate.getHours() + 0);
              const timeLabel = DateTime.fromJSDate(
                parseDateString(item.shift)
              ).toFormat("ha");
              return {
                id: item.id,
                title: `${item.first_name} ${item.last_name}`,
                start: parsedDate,
                end: endDate,
              };
            })}
            // makes sure that events can only be placed on 8AM or 8PM
            eventDrop={handleEventDrop}
          />
        </div>
        <div className="flex-1 max-w-2/5">
          <ScheduleTable schedule={schedule} />
        </div>
        {/* {schedule.map((item, index) => (
        <div key={index}>
          {`${item.first_name} ${item.last_name} - ${item.shift}`}
        </div>
      ))} */}
      </div>
    </>
  );
}
