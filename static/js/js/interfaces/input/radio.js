const radio = {
  html: ``,
  init: function(opts) {
    this.choices = opts.choices;
    html = "<div class='radio_group'>"
    for ([index, choice] of opts.choices.entries()) {
      html += `
        <label for="${this.id}_${index}">
          <input id="${this.id}_${index}" type="radio" name="${this.id}" value="${index}">
          ${choice}
        </label>`;
    }
    html += "</div>"
    this.target.html(html);
    this.target.find("input").checkboxradio();
    this.target.find("label:first-child input").prop("checked", true);    
    this.target.find("input").button("refresh");  
  },
  submit: function() {
    checked_val = this.target.find("input:checked").val();
    this.io_master.input(this.id, this.choices[checked_val]);
  },
  clear: function() {
    this.target.find("input").prop("checked", false);    
    this.target.find("label:first-child input").prop("checked", true);    
    this.target.find("input").button("refresh");  
  },
  load_example: function(data) {
    let child = this.choices.indexOf(data) + 1;
    this.target.find("input:nth-child("+child+")").prop("checked", true);
    this.target.find("input").button("refresh");  
  }
}
