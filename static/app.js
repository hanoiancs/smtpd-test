document.addEventListener("DOMContentLoaded", function(event) {
    new Vue({
        el: '#app',
        data: {
            mails: [],
            current_mail: null
        },
        mounted: function () {
            axios
                .get('/mails')
                .then(response => (response.status === 200 ? this.mails = response.data : this.mails = []))
        },
        methods: {
            show: function (idx) {
                this.current_mail = this.mails[idx];
            },
            fetch_next: function () {
                console.log('fetch next');
            },
            fetch_prev: function () {
                console.log('fetch prev');
            }
        }
    });
});