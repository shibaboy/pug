function TD_ch(num) {                                                                                 
    var TD_block = "Tab"+num;                                                                         
    var TDname1 = "TD"+num;                                                                           

    for(i=1;i<4;i++){                                                                                 
	var TD_num = "Tab"+i;                                                                                          
	var TDname2 = "TD"+i;                                                                                                 
	document.getElementById(TD_num).style.display="none";                                                          
	document.getElementById(TDname2).style.backgroundColor="#ffffff";                                                     
	document.getElementById(TDname2).style.fontSize="12";                                                                 
	document.getElementById(TDname2).style.fontWeight="normal";                                                           
    }                                                                                                                  
    document.getElementById(TD_block).style.display="block";                                                           
    document.getElementById(TDname1).style.backgroundColor="#B3CADF";                                                  
    document.getElementById(TDname1).style.fontWeight="bold";   
}
