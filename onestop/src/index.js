
import React from 'react'
import ReactDOM from 'react-dom'
import Navbar from './components/Navbar.js'
import MainContent from './components/MainContent.js'
import Footer from './components/Footer.js'

import './style.css'

// const element = <h1>Hello World</h1>;
// ReactDOM.render(element, document.getElementById('root'));



export default function APP(){
    return(
        <div>
            <Navbar />
            <MainContent />
            <Footer />
        </div>
    )
}

ReactDOM.render(<APP />, document.getElementById('root'));