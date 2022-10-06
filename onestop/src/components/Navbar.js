import React from "react"
// import search from "../images/search.svg"
import icon from "../images/icon.svg"

export default function navbar() {
    return (
        <div>
            <nav>
                <img id = "webIcon" width= "200" height = "50" src ={icon} alt = "icon"/> 
                <div class = "search">
                    {/* <img class = "searchIcon" src = {search} alt = "search icon" /> */}
                    <input
                    class = "searchBar"
                    type = "text" 
                    placeholder = "Where to?"/>

                </div>
            </nav>
        </div>
    )
}