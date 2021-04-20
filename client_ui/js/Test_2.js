function dic_to_str(dic_list) {
	let new_dic_list = []
	for (let i in dic_list){
		let dic = dic_list[i]
		let new_dic = {}
		new_dic.name = dic.name
		let arr = []
		for (let dic_key in dic.parm){
			arr.push(dic_key)
		}
		if(arr.length > 0){
			new_dic.parm = arr.toString()
		}
		else{
			new_dic.parm = 'None'
		}
		new_dic_list.push(new_dic)
	}
	return new_dic_list
}

const app = new Vue({
	el:"#app",
	data:{
		// 展示列表
		id_list:[],
		status_list:[],
		action_list:[],
		action_show_list:[],
		condition_list:[],
		condition_show_list:[],
		// 用户输入
		parm:{},
		name:'',
		skill:{},
		post_condition:{},
		pre_condition_list:[],
		subtree_list:[],
		subtree_show_list:[],

		goal_name:'',
		goal_parm:{},
		goal_condition:{},
		goal_condition_list:[],
		// 步骤标志
		active:0,

	},
	methods:{
		name_to_parm_action(event) {
			console.log('name_to_parm_action')
			for(let key in this.action_list){
				let item = this.action_list[key]
				if(item['name'] === event){
					this.parm = item['parm']
				}
			}
		},
		name_to_parm_condition(event) {
			console.log('name_to_parm_condition')
			for(let key in this.condition_list){
				let item = this.condition_list[key]
				if(item['name'] === event){
					this.parm = item['parm']
				}
			}
		},
		name_to_parm_goal(event) {
			console.log('name_to_parm_goal')
			for(let key in this.condition_list){
				let item = this.condition_list[key]
				if(item['name'] === event){
					this.goal_parm = item['parm']
				}
			}
		},
		action_next(){
			this.active++
			this.skill.name = this.name
			this.skill.parm = JSON.parse(JSON.stringify(this.parm))
			this.name = ''
			this.parm = {}
		},
		post_condition_next(){
			this.active++
			this.post_condition.name = this.name
			this.name = ''
		},
		pre_condition_next(){
			let pre_condition = {}
			pre_condition.name = this.name
			pre_condition.parm = JSON.parse(JSON.stringify(this.parm))
			this.pre_condition_list.push(pre_condition)
			this.name = ''
			this.parm = {}
		},
		// 将子树存储到列表
		subtree_commit() {
			this.pre_condition_next()
			let subtree = {'skill':JSON.parse(JSON.stringify(this.skill)),
							'post_condition':JSON.parse(JSON.stringify(this.post_condition)),
							'pre_condition_list':JSON.parse(JSON.stringify(this.pre_condition_list))}
			if(this.subtree_show_list.indexOf(subtree)){
				this.subtree_list.push(subtree)
			}
			else{
				this.$alert('这是一段内容', '标题名称', {
				  confirmButtonText: '确定',
				});
			}
			this.skill = {}
			this.post_condition = {}
			this.pre_condition_list = []
			this.active = 0
		},
		// 将存储过的子树发送到规划器
		subtree_list_submit() {
			console.log('subtree_list_submit')
			axios.post('http://localhost:5001/sendSubtreeList', this.subtree_list)
			.then(function (response) {
				console.log("response",response);
			})
			.catch(function (error) {
				console.log("error",error);
			});
		},
		// 将目标条件发送到规划器
		goal_submit() {
			console.log('goal_submit')
			this.goal_condition.name = this.goal_name
			this.goal_condition.parm = this.goal_parm
			axios.post('http://localhost:5001/sendGoalNode', this.goal_condition)
			.then(function (response) {
				console.log("response",response);
			})
			.catch(function (error) {
				console.log("error",error);
			});

		},
		start_submit(num) {
			console.log('start_submit')
			console.log('num',num)
			axios.get('http://localhost:5001/start_and_end?sig='+num)
			.then(function (response) {
				console.log("response",response);
			})
			.catch(function (error) {
				console.log("error",error);
			});

		},

	},
    created: function () {
		console.log('what??')
		// 应该加上一个从规划器获取子树列表的，但是与前端存储的不放在一起
		const that = this
		axios.get('http://localhost:5000/get_list')
			.then(function (response) {
				that.id_list = response.data[0]
				that.status_list = response.data[1]
				that.action_list = response.data[2]
				that.condition_list = response.data[3]
				console.log("/get", response)
				that.action_show_list = dic_to_str(that.action_list)
				that.condition_show_list = dic_to_str(that.condition_list)
				;
		})
		.catch(function (error) {
			console.log("error", error);
		});
		axios.get('http://localhost:5001/get_subtree_list')
			.then(function (response) {
				console.log(response.data)
				that.subtree_show_list = response.data
				;
		})
		.catch(function (error) {
			console.log("error", error);
		});
    },
})

