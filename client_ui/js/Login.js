const app = new Vue({
	el:"#app",
	data:{
		currentType:0,//判断个人或法人登录
		user:{},
		num: 0,
		num2: 0
	},
	methods:{
		//切换个人或法人登录  暂时只改变颜色 没啥用
		changeType1(){
			this.currentType=0
		},
		changeType2(){
			this.currentType=1
		},
		commit_1() {
			this.num2 = this.num + 1
		},
		//验证登录信息
		login(){
			console.log("this.user",this.user);
			// axios.post('http://localhost:8080/xu/user/login', this.user)
			// .then(function (response) {
			// 	console.log("response",response);
			// })
			// .catch(function (error) {
			// 	console.log("error",error);
			// });
			/*
			axios.post("http://localhost:8080/xu/user/login",this.user).then(res=>{
				console.log("res.data",res.data());
			});
			*/
		}
	}
})
