"use strict";
async function main(year) {
    const ID_res = await fetch(`/get_id/${year}`);
    const img = document.querySelector(".viewer");
    const settings_container = document.querySelector(".settings_container");
    const day_editor = document.querySelector(".day_editor");
    const back_btn = document.querySelector(".button.back");
    const next_btn = document.querySelector(".button.next");
    const premade_ctn = document.querySelector(".premade");
    const month_ctn = document.querySelector(".month");
    const day_ctn = document.querySelector(".day");
    const themes = (await (await fetch("/get_themes/theme")).json());
    const DayThemes = (await (await fetch("/get_themes/day")).json());
    const MonthThemes = (await (await fetch("/get_themes/month")).json());
    const DayEditorText = day_editor.querySelector(".day_editor_main");
    let focused_day = null;
    let current_days_locations = new Map();
    let current_month = 1;
    let current_theme_month = "default";
    let current_theme_day = "default";
    if (ID_res.status != 200) {
        return;
    }
    const ID = await ID_res.text();
    await change_image(ID, 1);
    back_btn.addEventListener("click", back);
    next_btn.addEventListener("click", next);
    async function change_image(id, month) {
        current_month = month;
        let date = Date.now().toString();
        img.src = `/image/${id}/${current_month}${focused_day === null ? "" : `/${focused_day}`}?${date.substring(date.length - 5, date.length)}`;
        current_days_locations = await (async () => {
            let map = new Map();
            Object.entries((await (await fetch(`/get_days/${id}/${current_month}`)).json())).forEach((value) => {
                map.set(JSON.parse(value[0]), value[1]);
            });
            return map;
        })();
    }
    async function reload_image() {
        let src = img.src;
        img.src = "";
        img.src = src;
    }
    async function next() {
        back_btn.classList.remove("disabled");
        next_btn.classList.remove("disabled");
        current_month += 1;
        if (current_month > 12) {
            current_month = 12;
            next_btn.classList.add("disabled");
            return;
        }
        await change_image(ID, current_month);
    }
    async function back() {
        back_btn.classList.remove("disabled");
        next_btn.classList.remove("disabled");
        current_month -= 1;
        if (current_month < 1) {
            current_month = 1;
            back_btn.classList.add("disabled");
            return;
        }
        await change_image(ID, current_month);
    }
    async function change_theme(theme) {
        await Promise.all([
            fetch(`/set_theme/day/${ID}/${theme.day}`),
            fetch(`/set_theme/month/${ID}/${theme.month}`),
        ]);
        await change_image(ID, current_month);
    }
    function generate_premade() {
        Object.entries(themes).forEach((value) => {
            let [name, [month, day]] = value;
            premade_ctn.innerHTML +=
                `<div class="cm-element" data-day="${day}" data-month="${month}" data-theme="${name}">${name.toProperCase()}</div>`;
        });
    }
    function generate_month() {
        MonthThemes.forEach((value) => {
            month_ctn.innerHTML +=
                `<div class="cm-element" data-month="${value}">${value.toProperCase()}</div>`;
        });
    }
    function generate_day() {
        DayThemes.forEach((value) => {
            day_ctn.innerHTML +=
                `<div class="cm-element" data-day="${value}">${value.toProperCase()}</div>`;
        });
    }
    generate_premade();
    generate_month();
    generate_day();
    function premade_onclick(e) {
        let month = this.dataset.month;
        let day = this.dataset.day;
        current_theme_day = day;
        current_theme_month = month;
        month_ctn.querySelectorAll(".cm-element").forEach(remove_selected);
        day_ctn.querySelectorAll(".cm-element").forEach(remove_selected);
        premade_ctn.querySelectorAll(".cm-element").forEach(remove_selected);
        month_ctn.querySelector(`[data-month="${month}"]`).classList.add("selected");
        day_ctn.querySelector(`[data-day="${day}"]`).classList.add("selected");
        this.classList.add("selected");
        change_theme({
            month: current_theme_month,
            day: current_theme_day,
        });
    }
    function day_onclick(e) {
        let day = this.dataset.day;
        current_theme_day = day;
        day_ctn.querySelectorAll(".cm-element").forEach(remove_selected);
        premade_ctn.querySelectorAll(".cm-element").forEach(remove_selected);
        day_ctn.querySelector(`[data-day="${day}"]`).classList.add("selected");
        this.classList.add("selected");
        change_theme({
            month: current_theme_month,
            day: current_theme_day,
        });
    }
    function month_onclick(e) {
        let month = this.dataset.month;
        current_theme_month = month;
        month_ctn.querySelectorAll(".cm-element").forEach(remove_selected);
        premade_ctn.querySelectorAll(".cm-element").forEach(remove_selected);
        month_ctn.querySelector(`[data-month="${month}"]`).classList.add("selected");
        this.classList.add("selected");
        change_theme({
            month: current_theme_month,
            day: current_theme_day,
        });
    }
    async function on_img_click(e) {
        var rect = e.target.getBoundingClientRect();
        var x = (e.clientX - rect.left) * (img.naturalWidth / this.clientWidth);
        var y = (e.clientY - rect.top) * (img.naturalHeight / this.clientHeight);
        let day = Array.from(current_days_locations.entries()).find((value) => value[0][0][0] <= x && x <= value[0][1][0] &&
            value[0][0][1] <= y && y <= value[0][1][1]);
        if (day && focused_day === null) {
            focused_day = day[1];
        }
        else {
            focused_day = null;
        }
        await change_image(ID, current_month);
        await manage_day_editor();
    }
    async function manage_day_editor() {
        if (focused_day === null) {
            day_editor.style.display = "none";
            settings_container.style.display = "";
        }
        else {
            DayEditorText.value = await fetch(`/get_text/${ID}/${current_month}/${focused_day}`).then((r) => r.json()).then((r) => r.message ? r.message : "").catch((e) => `Error: ${e}`);
            settings_container.style.display = "none";
            day_editor.style.display = "";
        }
    }
    async function send_text() {
        await fetch(`/set_text/${ID}/${current_month}/${focused_day}`, {
            method: "POST",
            body: JSON.stringify({
                message: DayEditorText.value.length ? DayEditorText.value : null,
            }),
        });
        await reload_image();
    }
    function remove_selected(e) {
        e.classList.remove("selected");
    }
    premade_ctn.querySelectorAll(".cm-element").forEach((el) => {
        el.addEventListener("click", premade_onclick);
    });
    month_ctn.querySelectorAll(".cm-element").forEach((el) => {
        el.addEventListener("click", month_onclick);
    });
    day_ctn.querySelectorAll(".cm-element").forEach((el) => {
        el.addEventListener("click", day_onclick);
    });
    img.addEventListener("click", on_img_click);
    document.querySelector(".day_editor_btn")?.addEventListener("click", send_text);
}
String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/g, function (txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
};
function load_year() {
    let y = Number(document.querySelector(".year_picker").value);
    document.querySelector(".viewer").classList.remove("hidden");
    document.querySelector(".year_chooser").classList.add("hidden");
    main(y);
}
