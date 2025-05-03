document.addEventListener("DOMContentLoaded", function () {
    const addWidgetBtn = document.getElementById("add-widget-btn");
    const widgetModal = document.getElementById("widget-modal");
    const closeModal = document.querySelector(".close");
    const widgetsContainer = document.getElementById("widgets-container");

    addWidgetBtn.addEventListener("click", function () {
        widgetModal.style.display = "block";
    });

    closeModal.addEventListener("click", function () {
        widgetModal.style.display = "none";
    });

    window.addCalendarWidget = function () {
        widgetModal.style.display = "none";

        if (!document.getElementById("calendar-widget")) {
            const calendarDiv = document.createElement("div");
            calendarDiv.id = "calendar-widget";
            calendarDiv.className = "widget calendar-widget";
            calendarDiv.style.left = "10px";
            calendarDiv.style.top = "10px";

            calendarDiv.innerHTML = `
                <div class="widget-header">
                    <span class="widget-title">📅 تقویم</span>
                    <span class="close-widget" onclick="removeWidget('calendar-widget')">✖</span>
                </div>
                <div id="persian-calendar"></div>
            `;

            widgetsContainer.appendChild(calendarDiv);
            loadCalendar();
            makeWidgetDraggable(calendarDiv);
            saveWidgetsState();
        }
    };

    window.removeWidget = function (widgetId) {
        const widget = document.getElementById(widgetId);
        if (widget) {
            widget.remove();
            saveWidgetsState();
        }
    };

    function loadCalendar() {
        const calendarElement = document.getElementById("persian-calendar");
        if (calendarElement) {
            const today = new Date();
        
            let options = {
                weekday: "long",
                day: "numeric",
                month: "long",
                year: "numeric"
            };
        
            let persianDate = new Intl.DateTimeFormat("fa-IR", options).format(today);
            calendarElement.innerHTML = `<p>${persianDate}</p>`;
        }
    }
    
    

    function makeWidgetDraggable(widget) {
        let offsetX, offsetY, isDragging = false;

        widget.addEventListener("mousedown", function (e) {
            isDragging = true;
            offsetX = e.clientX - widget.getBoundingClientRect().left;
            offsetY = e.clientY - widget.getBoundingClientRect().top;
            widget.style.zIndex = "1000";
        });

        document.addEventListener("mousemove", function (e) {
            if (isDragging) {
                const containerRect = widgetsContainer.getBoundingClientRect();
                const widgetRect = widget.getBoundingClientRect();

                let newLeft = e.clientX - offsetX - containerRect.left;
                let newTop = e.clientY - offsetY - containerRect.top;

                if (newLeft < 0) newLeft = 0;
                if (newTop < 0) newTop = 0;
                if (newLeft + widgetRect.width > containerRect.width) {
                    newLeft = containerRect.width - widgetRect.width;
                }
                if (newTop + widgetRect.height > containerRect.height) {
                    newTop = containerRect.height - widgetRect.height;
                }

                widget.style.left = `${newLeft}px`;
                widget.style.top = `${newTop}px`;
            }
        });

        document.addEventListener("mouseup", function () {
            if (isDragging) {
                isDragging = false;
                saveWidgetsState();
            }
        });
    }

    function saveWidgetsState() {
        const widgets = document.querySelectorAll(".widget");
        const widgetData = [];

        widgets.forEach(widget => {
            widgetData.push({
                id: widget.id,
                left: widget.style.left,
                top: widget.style.top
            });
        });

        localStorage.setItem("widgetsState", JSON.stringify(widgetData));
    }

    function loadWidgetsState() {
        const savedWidgets = JSON.parse(localStorage.getItem("widgetsState"));

        if (savedWidgets) {
            savedWidgets.forEach(widgetInfo => {
                if (widgetInfo.id === "calendar-widget") {
                    addCalendarWidget();
                }

                const widget = document.getElementById(widgetInfo.id);
                if (widget) {
                    widget.style.position = "absolute";
                    widget.style.left = widgetInfo.left;
                    widget.style.top = widgetInfo.top;
                }
            });
        }
    }

    loadWidgetsState();
});
