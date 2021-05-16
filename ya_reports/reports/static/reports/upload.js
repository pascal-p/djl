const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
const alertBox = document.getElementById('alert-box')

Dropzone.autoDiscover = false;

const handleAlerts = (type, msg) => {
  alertBox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
      ${msg}
    </div>
  `;
}

const yaDropzone = new Dropzone('#ya-dropzone', {
  url: 'reports/upload/',
  init: function() {
    this.on('sending', function(file, xhr, formData) {
      console.log('sending');
      formData.append('csrfmiddlewaretoken', csrf)
    })
    this.on('success', function(file, resp) {
      console.log(resp);
      const ex = resp.ex;
      if (ex) {
        handleAlerts('danger', 'File already exists')
      }
      else {
        handleAlerts('success', 'Your File has been uploaded')
      }
    })
  },
  maxFiles: 3,
  maxFilesize: 3, // MB
  acceptedFiles: '.csv'
})
