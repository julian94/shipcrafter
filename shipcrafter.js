var app = new Vue({
	el: '#app',
	data: {message: 'Hello Vue!'}
})
var shipList = new Vue({
	el: '#shipList',
	data: {
		ships: [] // Fetch data/list.json
	},
	created () {
		this.fetchData()
	},
	methods: {
		fetchData () {
			this.ships = 
		}
	}
})