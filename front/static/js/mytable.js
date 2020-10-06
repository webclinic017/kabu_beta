var app ={}||app;
app ={
	columns			: [],
	head			: '',
	data			: '',
	target  		: '',
	//初期化
	init			:function(){
		if(app.valiadtion()){
			for(var i =0 ;i<app.columns.length ; i++){
				
				var node =''
				var obj  = app.columns[i];
				var tr   = ''
				var dataobj =app.data[obj.name];
				
				if(obj.hasOwnProperty('isheader')){
					node   = app.setHeadHtml(dataobj);
					tr     = app.setHeadRowHtml(obj.label,node);
				}else{
					
					var percentlist =app.convert_percent(dataobj)
					node   			= app.setBodyHtml(dataobj,percentlist);
					tr 	   			= app.setRowHtml(obj.label,node);
				}
				
				app.addToTarget(tr);
			}
			
		}
	},
	//percentを返す
    convert_percent : function(data){
    	//初期化
    	result=[0];
    	if(data.length <=1){
    		return result;
    	}
    	
    	for(var i=1;i<data.length;i++){
    		//後の数字を前の数字を割る
	    		percent = (data[i]-data[i-1])/data[i-1]
	    		
	    		result.push(percent.toFixed(3)*100)
	    	}
	    	return result
    },
    //valiation
    valiadtion 		: function(){
    	var flag =true;
    	
    	return flag;
    },
    //テーブルbody追加する
    setBodyHtml:function(data,percentlist){
    	var html =''
    	for(var i= 0; i<data.length; i++){
    		var classstr    = ''
    		if(percentlist[i] >0){
    			classstr = 'class ="plus"'
    		}else if(percentlist[i] <0){
    			classstr = 'class ="minus"'
    		}
    		
    		html +='<td '+ classstr +'>';
    		html +=data[i];
    		if(percentlist[i] !==0){
    			html +=' ('+percentlist[i]+'%)';
    		}
    		
    		html +='</td>';
    	}
    	
    	return html; 
    },
  //テーブルHEAD追加する
    setHeadHtml:function(data){
    	var html =''
    	for(var i= 0; i<data.length; i++){
    		html +='<th>';
    		html +=data[i]
    		html +='</th>';
    	}
    	
    	return html; 
    },
  //テーブルHEAD追加する
    setRowHtml:function(lable,html){
    	result ='<tr>';
    	result +='<td>'+lable +'</td>';
    	result +=html;
    	result +='</tr>';
    	
    	return result; 
    },
  //テーブルHEAD追加する
    setHeadRowHtml:function(lable,html){
    	result ='<tr>';
    	result +='<th>'+lable +'</th>';
    	result +=html;
    	result +='</tr>';
    	
    	return result; 
    },
    //テーブルに追加する
    addToTarget :function(html){
    	$(app.target).append(html);		
    }
    
	};



