const app = new Vue({
	el:"#app",
	data:{
		isagree:false,
		username:"",//注册的用户名
		usertel:"",//注册的用户手机号
		userpassword1:"",//注册的用户密码
		userpassword2:"",//确认密码
		
	},
	methods:{
		//验证信息是否填写完整  成功则跳转到实名认证界面
		register(){
			if(this.username===""){
				alert("请填写用户名")
			}else if(this.usertel===""){
				alert("请填写手机号码")
			}else if(this.userpassword1===""){
				alert("请填写密码")
			}else if(this.userpassword2===""){
				alert("请确认密码")
			}else if(this.userpassword2!=this.userpassword1){
				alert("密码不一致")
			}else if(!this.isagree){
				alert("请先阅读并同意网站协议")
			}else{
				alert("注册成功 请在登陆页登录")
				window.location.href = 'RealName.html'
			}
			
		}
	}
})
