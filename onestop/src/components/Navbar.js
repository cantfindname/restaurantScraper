import React, { useEffect} from "react";
import { useForm } from "react-hook-form";
import { useState } from "react";
// import search from "../images/search.svg"
import icon from "../images/icon.svg";
import axios from "axios";

export default function Navbar(props) {
    const { register, formState: { errors }, handleSubmit } = useForm();
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

    function onSubmit(data) {
        console.log(data.keyword)
        fetchSearch(data.keyword)
    }

    function fetchSearch(keyword) {
        axios.get("http://localhost:3001/search", {params: {keyword: keyword}})
        .then(
            response => 
            // console.log(response)
            // after we get here, then we can send the data to our page
            props.setSearchedRestaurants(response.data)
        )
    }

    // if the input is empty, you want to set props.setSearchedRestaurants([])


    return (
        <div>
            <nav>
                <img id = "webIcon" width= "200" height = "50" src ={icon} alt = "icon"/> 
                <div class = "search">
                    {/* <img class = "searchIcon" src = {search} alt = "search icon" /> */}
                    <form onSubmit={handleSubmit(onSubmit)}>
                  
                        <input
                        class = "searchBar"
                        name = "keyword"
                        type = "text" 
                        placeholder = "Where to?"
                        {...register("keyword", { required: true })} 
                        />
                    
                        <input type="submit" value ="Search"/>
                    </form>

                </div>
            </nav>
        </div>
    )
}