import React, { useEffect} from "react";
import { useState } from "react";
// import search from "../images/search.svg"
import icon from "../images/icon.svg";
import Axios from "axios";

export default function Navbar() {

    // const [resData, setResData] = useState([{}])
    // useEffect (()=>{
    //     fetch("http://localhost:3001/api/get").then(
    //         response => response.json()
    //     ).then(
    //         data => {
    //             setResData(data)
    //         }
    //     )
    // }, [])
    
    const searchHandle =(event)=>{
        console.warn(event.target.value);
    }

    return (
        <div>
            <nav>
                <img id = "webIcon" width= "200" height = "50" src ={icon} alt = "icon"/> 
                <div class = "search">
                    {/* <img class = "searchIcon" src = {search} alt = "search icon" /> */}
                    <input
                    class = "searchBar"
                    type = "text" 
                    placeholder = "Where to?"
                    onChange={searchHandle}/>

                </div>
            </nav>
        </div>
    )
}