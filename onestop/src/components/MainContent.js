import React, {useState, useEffect} from "react"
import RestaurantCard from "./RestaurantCard"

export default function Main_content() {
    const [resData, setResData] = useState(null)

    const fetchResData = () => {
        fetch('http://localhost:3001/api/get')
        .then(response =>response.json())
        .then(resData => (
        setResData(resData)))
        .catch(err => console.log(err))
    }
    useEffect(() => fetchResData(), [])


    // useEffect (()=>{
    //     fetch('http://localhost:3001/api/get')
    //     .then(response => response.json())
    //     .then(resData => setResData(JSON.parse(resData)))
    // }, [])
    console.log("i am right before return in main content")
    console.log(resData)
    return (
        <div className="main">
            <div className="sort">
                Sort By:
                <button>Popularity</button>
                <button>Rating</button>
                <button>Distance</button>
            </div>
            <div class = "restaurantList">
                {resData && resData.map((resData)=>
                <RestaurantCard props={resData}/>
                )}
           
            </div>
        </div>

    )
}