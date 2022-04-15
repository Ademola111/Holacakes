/* 
this is a javascript page
Authour: Onayemi Hakeem AdemolaCode
Date: 7th February, 2022
P rogram: External JS Demo
*/

document.body.style.backgroundColor="skyblue";
// program to print numbbrs from 110 to 210 using for loop

for(var number=110; number <=210; number++){
	document.write("<div>"+ number + "</div>")
}

//program to print multiple of 5 from 5 to 100
for(var k=5; k <=100; k=k+5){
	document.write(k + ", ");
}

//program to display my favourite statement five times 
for(var slogan="Diginity is earned through hardwork", j=0; j <5; j++){
	document.write("<div>" + slogan +"</div>" );
}

for(var b=1; b<=5; b++){
	document.write("<div>" + "Life is good" +"</div>" );
}

//while loop syntax
var year = 1914;
while(year < 2023){
	document.write(year + " ");
	year++;
}

//do while loop syntax
var myyear = 2022; //initializer
do{
	document.write("<div>" + myyear + "</div>");
	myyear--; //decrement to stop it

}while(myyear >= 1914); //condition

//odd number between 1 and 10
var myyear = 1; //initializer
do{
	document.write(myyear + " ");
	myyear+=2; //decrement to stop it

}while(myyear < 10); //condition


var mynum = 1;
while(mynum <= 10){
	if(mynum%2 == 0){
		document.write("<br>" + mynum +'even number');
	}else{
		document.write(mynum +'odd number <br>');
	}

	mynum++;
}
