const checkbox = {
  html: `
    <div class="checkbox_solo">
      <label class='holder'><input class="checkbox" type="checkbox">&nbsp;</label>
      <div class="interpretation interpret_sub"></div>
    </div>`,
  init: function(opts) {
    this.target.find("input").checkboxradio();    
  },
  show_interpretation: function(data) {
    let html = ""
    for (let i = 0; i < data.length; i++) {
      let score = data[i];
      let mark = ["&#x2717;", "&#x2713;"][i];
      if (score == null) {
        html += `<div class='interpret_check interpret_select'>
          ${mark}
        </div>`
      } else {
        html += `<div class='interpret_check' title='${score}'
        style='background-color: ${getSaliencyColor(score)}'>
          ${mark}
        </div>`
      }
    }
    this.target.find(".interpretation").html(html);
  },
  submit: function() {
    let io = this;
    let is_checked = this.target.find("input").prop("checked")
    this.io_master.input(this.id, is_checked);
  },
  clear: function() {
    this.target.find(".interpretation").empty();    
    this.target.find("input").prop("checked", false);    
    this.target.find("input").button("refresh");  
  },
  load_example: function(data) {
    if (data) {
      this.target.find("input").prop("checked", true);
    } else {
      this.target.find("input").prop("checked", false);
    }
    this.target.find("input").button("refresh");  
  }
}
