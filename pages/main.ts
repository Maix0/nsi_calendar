async function main(year: number) {
    const ID_res = await fetch(`/get_id/${year}`)
    const img = document.querySelector(".viewer") as HTMLImageElement;
    const back_btn = document.querySelector(".button.back") as HTMLButtonElement
    const next_btn = document.querySelector(".button.next") as HTMLButtonElement
    const premade_ctn = document.querySelector(".premade") as HTMLDivElement
    const month_ctn = document.querySelector(".month") as HTMLDivElement
    const day_ctn = document.querySelector(".day") as HTMLDivElement
    const themes = (await (await fetch("/get_themes/theme")).json());
    const DayThemes = (await (await fetch("/get_themes/day")).json());
    const MonthThemes = (await (await fetch("/get_themes/month")).json());

    let current_month = 1;
    let current_theme_month = "default";
    let current_theme_day = "default";
    if (ID_res.status != 200) {
        return
    }
    const ID = await ID_res.text()
    change_image(ID, 1)
    back_btn.addEventListener("click", back)
    next_btn.addEventListener("click", next)

    function change_image(id: String, month: number) {
        current_month = month;
        let date = Date.now().toString();
        img.src = `/image/${id}/${current_month}?${date.substring(date.length - 5, date.length)}`
    }

    function reload_image() {
        let src = img.src
        img.src = ""
        img.src = src
    }

    function next() {
        back_btn.classList.remove("disabled")
        next_btn.classList.remove("disabled")

        current_month += 1;
        if (current_month > 12) {
            current_month = 12
            next_btn.classList.add("disabled")
        }
        change_image(ID!, current_month)
    }

    function back() {
        back_btn.classList.remove("disabled")
        next_btn.classList.remove("disabled")

        current_month -= 1;
        if (current_month < 1) {
            current_month = 1
            back_btn.classList.add("disabled")
        }
        change_image(ID!, current_month)
    }

    async function change_theme(theme: {
        month: string | null,
        day: string | null
    }) {
        await Promise.all([fetch(`/set_theme/day/${ID}/${theme.day}`), fetch(`/set_theme/month/${ID}/${theme.month}`)])

        change_image(ID!, current_month)
    }

    function generate_premade() {
        Object.entries(themes).forEach((value: any) => {
            let [name, [month, day]] = value;
            premade_ctn.innerHTML += `<div class="cm-element" data-day="${day}" data-month="${month}" data-theme="${name}">${name.toProperCase()}</div>`
        });
    }

    function generate_month() {
        MonthThemes.forEach((value: any) => {
            month_ctn.innerHTML += `<div class="cm-element" data-month="${value}">${value.toProperCase()}</div>`
        });
    }

    function generate_day() {
        DayThemes.forEach((value: any) => {
            day_ctn.innerHTML += `<div class="cm-element" data-day="${value}">${value.toProperCase()}</div>`
        });
    }

    generate_premade()
    generate_month()
    generate_day()

    function premade_onclick(this: HTMLDivElement, e: MouseEvent) {
        let month = this.dataset.month!;
        let day = this.dataset.day!
        current_theme_day = day
        current_theme_month = month

        month_ctn.querySelectorAll(".cm-element").forEach(remove_selected)
        day_ctn.querySelectorAll(".cm-element").forEach(remove_selected)
        premade_ctn.querySelectorAll(".cm-element").forEach(remove_selected)

        month_ctn.querySelector(`[data-month="${month}"]`)!.classList.add("selected")
        day_ctn.querySelector(`[data-day="${day}"]`)!.classList.add("selected")
        this.classList.add("selected")
        change_theme({ month: current_theme_month, day: current_theme_day })
    }

    function day_onclick(this: HTMLDivElement, e: MouseEvent) {
        let day = this.dataset.day!
        current_theme_day = day
        day_ctn.querySelectorAll(".cm-element").forEach(remove_selected)
        premade_ctn.querySelectorAll(".cm-element").forEach(remove_selected)
        day_ctn.querySelector(`[data-day="${day}"]`)!.classList.add("selected")

        this.classList.add("selected")
        change_theme({ month: current_theme_month, day: current_theme_day })
    }

    function month_onclick(this: HTMLDivElement, e: MouseEvent) {
        let month = this.dataset.month!
        current_theme_month = month
        month_ctn.querySelectorAll(".cm-element").forEach(remove_selected)
        premade_ctn.querySelectorAll(".cm-element").forEach(remove_selected)
        month_ctn.querySelector(`[data-month="${month}"]`)!.classList.add("selected")
        this.classList.add("selected")
        change_theme({ month: current_theme_month, day: current_theme_day })
    }

    function remove_selected(e: Element) {
        e.classList.remove("selected")
    }
    premade_ctn.querySelectorAll(".cm-element").forEach(el => {
        (el as HTMLDivElement).addEventListener("click", premade_onclick)
    })
    month_ctn.querySelectorAll(".cm-element").forEach(el => {
        (el as HTMLDivElement).addEventListener("click", month_onclick)
    })
    day_ctn.querySelectorAll(".cm-element").forEach(el => {
        (el as HTMLDivElement).addEventListener("click", day_onclick)
    })
}


String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/g, function (txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
};


function load_year() {
    let y = Number((document.querySelector(".year_picker") as HTMLInputElement).value)
    document.querySelector(".viewer")!.classList.remove("hidden")
    document.querySelector(".year_chooser")!.classList.add("hidden")

    main(y)
}