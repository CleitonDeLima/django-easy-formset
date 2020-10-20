class Formset {
  static undoHTML = '<a href="#">Undo</a>'
  static FORMSET_ADD = "formset-add"
  static FORMSET_FORMS = "formset-forms"
  static FORMSET_EMPTY_FORM = "formset-empty-form"
  static FORMSET_DELETE = "formset-form-delete"

  constructor(prefix) {
    this.prefix = prefix
    this.nested = []

    this.container = document.getElementById(this.prefix)

    if (this.container === null) throw Error(`Formset prefix "${this.prefix}" not exists.`)

    this.addButton = this.container.querySelector(`[${Formset.FORMSET_ADD}=${this.prefix}]`)
    this.formsContainer = this.container.querySelector(`[${Formset.FORMSET_FORMS}=${this.prefix}]`)
    this.emptyForm = this.container.querySelector(`[${Formset.FORMSET_EMPTY_FORM}=${this.prefix}]`)
    this.addButton.addEventListener("click", this.handleAdd.bind(this))

    this.updateForms()
    this.forms.forEach(form => this.updateDeleteButton(form))
  }

  handleAdd(event) {
    event.preventDefault()

    if (this.maxForms === this.totalForms) return

    const clone = this.emptyForm.content.cloneNode(true)
    const newForm = document.createElement("div")
    newForm.setAttribute("formset-form", "")
    newForm.appendChild(clone)

    newForm.querySelectorAll("*").forEach(el => {
      this.updateElementIndex(el, this.prefix, this.totalForms)
    })
    this.formsContainer.appendChild(newForm)
    this.totalForms++
    this.updateForms()

    this.updateDeleteButton(newForm)

    const addEvent = new CustomEvent("formset:add", { detail: { form: newForm } })
    document.dispatchEvent(addEvent)
  }

  handleDelete(event) {
    event.preventDefault()

    if (this.minForms === this.totalForms) return

    const form = event.target.closest("[formset-form]")

    const deletedEvent = new CustomEvent("formset:deleted", {
      detail: { form: form }
    })
    document.dispatchEvent(deletedEvent)

    // checkbox when field id is filled
    const id = form.querySelector("[name$=-id]")
    if (id && id.value) {
      form.querySelector("[name$=-DELETE]").checked = true

      this.showOrHiddenChildren(form, true)

      // create undo element
      const revertElement = this.createElement(Formset.undoHTML)
      revertElement.setAttribute("formset-undo", "")
      revertElement.addEventListener("click", this.handleRestore.bind(this))

      form.append(revertElement)
      form.setAttribute("formset-form-excluded", "")
      form.removeAttribute("formset-form")

      return
    }

    // remove form
    form.remove()

    // update total forms
    this.totalForms--

    // update idxs
    this.forms.forEach((form, idx) => {
      form.querySelectorAll("*").forEach(el => {
        this.updateElementIndex(el, this.prefix, idx)
      })
    })

    this.updateForms()
  }

  handleRestore(event) {
    event.preventDefault()

    const form = event.target.closest("[formset-form-excluded]")
    form.querySelector("[formset-undo]").remove()
    this.showOrHiddenChildren(form, false)

    form.querySelector("[name$=-DELETE]").checked = false
    form.removeAttribute("formset-form-excluded")
    form.setAttribute("formset-form", "")
  }

  updateDeleteButton(form) {
    const checkDelete = form.querySelector("[name$=-DELETE]")
    const btnDel = this.btnDelete(form)
    const hasDelete = checkDelete !== null

    if (hasDelete) {
      btnDel.addEventListener("click", this.handleDelete.bind(this))
      checkDelete.hidden = true
    }
  }

  updateForms() {
    this.addButton.hidden = this.maxForms === this.totalForms

    this.forms.forEach((form, index) => {
      const checkDelete = form.querySelector("[name$=-DELETE]")
      const labelDelete = form.querySelector("[for$=-DELETE]")
      const hasDelete = checkDelete !== null

      if (labelDelete)
        labelDelete.hidden = true

      form.setAttribute("form-index", index)
      this.btnDelete(form).hidden = this.minForms === this.totalForms || !hasDelete

      this.instanceNested(form)
    })
  }

  instanceNested(form) {
    const formsets = form.querySelectorAll("[formset-is-nested]") // TODO: get one level
    if (formsets === null) return

    formsets.forEach(formset => {
      const nestedPrefix = formset.getAttribute("id")
      const hasInstance = Boolean(this.nested.filter(f => f.prefix === nestedPrefix).length)

      if (!hasInstance) {
        this.nested.push(new Formset(nestedPrefix))
      }
    })
  }

  showOrHiddenChildren(form, hidden) {
    form.childNodes.forEach(node => node.hidden = hidden)
  }

  updateElementIndex(el, prefix, newIdx) {
    const idRegex = new RegExp(`(${prefix}-(\\d+|__prefix__))`, "g")
    const replacement = `${prefix}-${newIdx}`

    if (el.hasAttribute("for")) {
      const newAttr = el.getAttribute("for").replace(idRegex, replacement)
      el.setAttribute("for", newAttr)
    }

    if (el.id) {
      el.id = el.id.replace(idRegex, replacement)
    }
    if (el.name) {
      el.name = el.name.replace(idRegex, replacement)
    }

    if (el instanceof HTMLTemplateElement) {
      el.innerHTML = el.innerHTML.replace(idRegex, replacement)
    }

    [
      Formset.FORMSET_ADD,
      Formset.FORMSET_EMPTY_FORM,
      Formset.FORMSET_FORMS,
      Formset.FORMSET_DELETE
    ].forEach(attr => {
      if (el.hasAttribute(attr))
        el.setAttribute(attr, el.getAttribute(attr).replace(idRegex, replacement))
    })
  }

  createElement(stringHTML) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(stringHTML, "text/html");
    return doc.body.firstElementChild;
  }

  btnDelete(form) {
    const index = form.getAttribute("form-index")
    return form.querySelector(`[${Formset.FORMSET_DELETE}=${this.prefix}-${index}]`)
  }

  get totalForms() {
    const value = this.container.querySelector(`[name=${this.prefix}-TOTAL_FORMS]`).value
    return Number(value)
  }

  set totalForms(value) {
    this.container.querySelector(`[name=${this.prefix}-TOTAL_FORMS]`).value = value
  }

  get minForms() {
    const value = this.container.querySelector(`[name=${this.prefix}-MIN_NUM_FORMS`).value
    return Number(value)
  }

  get maxForms() {
    const value = this.container.querySelector(`[name=${this.prefix}-MAX_NUM_FORMS`).value
    return Number(value)
  }

  get forms() {
    return this.formsContainer.querySelectorAll(":scope > [formset-form]")
  }
}
