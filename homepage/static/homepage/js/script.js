function movekatalog() {
	let a = document.querySelector('.katalogi')
	if (a.style.top === '62px') {
		a.style.top = '-130%'
		// a.style.border = '1px rgba(225,225,225,0.3) solid';
		// a.style.borderTop= '0.1px rgba(0,0,0,0.3) solid';
		// a.style.borderBottom = '1px rgba(0,0,0,0.3) solid';
	} else {
		a.style.top = '62px'
		// a.style.border = '240px #FFF solid';
		// a.style.borderTop= '10px #FFF solid';
		// a.style.borderBottom = '200px #FFF solid';
	}
}

function showkatalog(i) {
	let x = document.querySelectorAll('.list-katalog-list');

	for (let i of x) {
		i.classList.remove('show');
		i.parentElement.style.backgroundColor = '#fff'
	}

	let a = document.querySelector(`.${i}`)
	a.classList.add('show');
	a.parentElement.style.backgroundColor = '#d3d3d3'
}


/* конфигурация */
let width = 203;
let count = 1;
let position = 0;


function showleftbar() {
	let a = document.querySelector('.left-bar')
	a.classList.toggle('show-bar')
	let b = document.querySelector('.mobile-petviy-stupen  .katalog')
	let c = document.querySelector('.close-bar')
	if (b.style.display === 'block') {
		b.style.display = 'none'
		c.style.display = 'block'
	} else {
		b.style.display = 'block'
		c.style.display = 'none'
	}
}


// var b = 0
// function moveqlavniytovarright() {
// 	let a = document.querySelectorAll('.qlavniy-tovar')
// 	let c = document.querySelector('.slayd')
//
// 	b -= 203
// 	c.style.left = `${b}px`
// 	console.log(b)
// }
//
// function moveqlavniytovarleft() {
// 	let a = document.querySelectorAll('.qlavniy-tovar')
// 	let c = document.querySelector('.slayd')
//
// 	b += 203
// 	c.style.left = `${b}px`
// 	console.log(b)
// }
//



function showpoiskovik() {
	let a = document.querySelector('.mobile-poiskovik')
	a.classList.toggle('show-poisk')
}

function mobileshowkatalog() {
	let a = document.querySelector('.mobile-list-katalog-tovarov')
	let c = document.querySelector('.mobile-list-katalog-tovarov ul')
	let b =document.querySelectorAll('.praviy-katalog')
	a.classList.toggle('showmlk')
	if ('showmlk' === a.className.split(' ')[1]) {
		for(let i = 0; i<b.length; i++) {
			let pkatalog = b[i]
			pkatalog.style.right = '-100%'
		}
		c.style.left = '0'

	}

}

function showpraviykatalog(i) {
	let a = document.querySelector(".mobile-list-katalog-tovarov ul")
	let b = document.querySelector(`.${i}`)
	a.style.left = '-100%'
	b.style.right = '3.8vw'
}

function backtokatalog(i) {
	let a = document.querySelector(".mobile-list-katalog-tovarov ul")
	let b = document.querySelector(`.${i}`)
	b.style.right = '-100%'
	a.style.left = '0'
}

const perexodi = document.querySelector('.perexodi-iz-mainpg')
function showperexodi() {
	alert(5)
	perexodi.style.display = 'flex'
}



// function moveqlavniytovarright() {
// 	let slayd = document.querySelector('.slayd')
// 	let a = getComputedStyle(slayd).width.split('px')
// 	a = a.join('')
// 	console.log(a)
// 	let b = document.querySelectorAll('.qlavniy-tovar').length
// 	console.log(a/b)
// }


const secondForm = document.querySelector('.main-of-salers .second')
const firstForm = document.querySelector('.main-of-salers .first')

const name = document.querySelector('.main-of-salers .name input'),
	surname = document.querySelector('.main-of-salers .surname input'),
	dataOfBirth = document.querySelector('.main-of-salers .data-of-birth input'),
	email = document.querySelector('.main-of-salers .email input'),
	mobilNumber = document.querySelector('.main-of-salers .mobil-numb input'),
	occumation = document.querySelector('.main-of-salers .occupation input'),
	address = document.querySelector('.main-of-salers .address input')
let formInputs = document.querySelectorAll('.main-of-salers input')
formInputs.forEach(formInput => formInput.addEventListener('blur', (event) => {
	if (formInput.value === '') {
		formInput.style.border = '2px red solid'
	} else {
		formInput.style.border = '2px green solid'
	}
}))

function nextForm() {
	let name = document.querySelector('.main-of-salers .name input').value,
		surname = document.querySelector('.main-of-salers .surname input').value,
		dataOfBirth = document.querySelector('.main-of-salers .data-of-birth input').value,
		email = document.querySelector('.main-of-salers .email input').value,
		mobilNumber = document.querySelector('.main-of-salers .mobil-numb input').value,
		occumation = document.querySelector('.main-of-salers .occupation input').value,
		address = document.querySelector('.main-of-salers .address input').value;

	document.querySelector('.infa .name').innerHTML = name;
	document.querySelector('.infa  .surname').innerHTML = surname;
	document.querySelector('.infa  .data-of-birth').innerHTML = dataOfBirth;
	document.querySelector('.infa  .email').innerHTML = email;
	document.querySelector('.infa .mobil-numb').innerHTML = mobilNumber;
	document.querySelector('.infa .occupation').innerHTML = occumation;
	document.querySelector('.infa .address').innerHTML = address;


	let formInputs = document.querySelectorAll('.main-of-salers  .first  input')
	let count = 0
	formInputs.forEach(formInput => {
		if (formInput.value === '') {
			formInput.style.border = '2px red solid'
		} else if (formInput.value !== '') {
			formInput.style.border = '2px green solid'
			count +=1
		}
		if (count >=8) {
			firstForm.style.left = '-100%'
			secondForm.style.right = '0'
		}
	})
}
function backForm() {
	firstForm.style.left = '0'
	secondForm.style.right = '-100%'
}


// function nextForm() {
// 	let count = 0
// 	let formInputs = document.querySelectorAll('.main-of-salers input')
// 	formInputs.forEach(formInput => {
// 		if (formInput.value === '') {
// 			count +=1
// 			formInput.style.border = '2px red solid'
// 		} else if (count === 7) {
// 			formInput.style.border = '2px green solid'
// 			firstForm.style.left = '-100%'
// 			secondForm.style.right = '0'
// 		}
// 	})
// }















function  usloviye() {
	let UsloviyeInput = document.querySelector('.checkbox-uslov input[type="checkbox"]')
	if (UsloviyeInput.checked === true) {
		document.querySelector('.zareq-button').removeAttribute('disabled' )
	} else {
		document.querySelector('.zareq-button').setAttribute('disabled', true)
	}
}

const tovarLeftPhotos = document.querySelectorAll('.tovar-photo-change')
tovarLeftPhotos.forEach(tovarLeftPhoto => tovarLeftPhoto.addEventListener('click', (event) => {
	let a = event.target
	let imgSrc = a.src
	let mainPhoto = a.closest('.tovar-photos').querySelector('.main-photo img')
	mainPhoto.style.opacity = '0'
	mainPhoto.style.transition = '0.4s'
	setTimeout(()=>{
		mainPhoto.src = imgSrc
		mainPhoto.style.opacity = '1'
	},400)

}))



function showAddBar() {
	let leftAddBar = document.querySelector('.add-left-bar')
	let divTexts = document.querySelectorAll('.add-left-bar>ul>li>.left>div')
	let leftIconOfAngels = document.querySelectorAll('.add-left-bar>ul>li>i')
	divTexts.forEach(divText => {
		if (divText.style.display !== 'none') {
			divText.style.display = 'none';
			divText.style.opacity = '0';
		} else {
			divText.style.display = 'block';
			divText.style.opacity = '1';
		}
	})
	leftIconOfAngels.forEach(leftIconOfAngel => {
		if (leftIconOfAngel.style.display !== 'none') {
			leftIconOfAngel.style.display = 'none';
			leftAddBar.style.width = '55px';
		} else {
			leftIconOfAngel.style.display = 'block';
			leftIconOfAngel.style.opacity = '1';
			leftAddBar.style.width = '213px';
		}
	})
}
function showAddBarm() {
	let leftAddBar = document.querySelector('.add-left-bar')
	let divTexts = document.querySelectorAll('.add-left-bar>ul>li>.left>div')
	let leftIconOfAngels = document.querySelectorAll('.add-left-bar>ul>li>i')
	divTexts.forEach(divText => {

			divText.style.display = 'block';
			divText.style.opacity = '1';

	})
	leftIconOfAngels.forEach(leftIconOfAngel => {

			leftIconOfAngel.style.display = 'block';
			leftIconOfAngel.style.opacity = '1';
			leftAddBar.style.width = '213px';

	})
}
function hideAddBarm() {
	let leftAddBar = document.querySelector('.add-left-bar')
	let divTexts = document.querySelectorAll('.add-left-bar>ul>li>.left>div')
	let leftIconOfAngels = document.querySelectorAll('.add-left-bar>ul>li>i')
	divTexts.forEach(divText => {
		divText.style.display = 'none';
		divText.style.opacity = '0';
	})
	leftIconOfAngels.forEach(leftIconOfAngel => {
		leftIconOfAngel.style.display = 'none';
		leftAddBar.style.width = '55px';
	})
}

function previewFile(file) {
	console.log(this)
	let img = file.parentElement
	try {
		img.querySelector('label').remove()
	} catch  {
	}
	let reader = new FileReader();

	reader.readAsDataURL(file.files[0]);
	reader.onload = function () {
		img.style.backgroundImage = `url("${reader.result}")`
		img.style.border = 'none'
	}
	let a = document.querySelector('.del-img')
	a.style.display = 'flex'


}

function delPhoto(i) {
	let input = i.parentElement.querySelector('input')
	let img =  i.parentElement
	let n = img.classList[1]
	let delIco = i
	delIco.remove()
	input.value = ''
	img.style.backgroundImage = ''
	img.style.border = '2px #000 solid'
	let label = `<label for='forfile${n}'><i class="fas fa-plus"></i></label>`
	img.innerHTML += label
}


function showSecondForm(i) {
	i.remove()
	let secondForm = document.querySelector('.second-form')
	secondForm.style.display = 'block'
}
