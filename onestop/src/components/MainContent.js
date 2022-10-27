import React, {useState, useEffect} from "react"
import RestaurantCard from "./RestaurantCard"

export default function Main_content() {

    // const [resData, setResData] = useState(null)

    // const fetchResData = () => {
    //     fetch('http://localhost:3001/api/get')
    //     .then(response =>response.json())
    //     .then(resData => setResData(Object.values(resData.dat)))
    //     .catch(err => console.log(err))
    // }
    
    // useEffect(() => fetchResData(), [])


    const [resData, setResData] = useState([{}])
    useEffect (()=>{
        fetch("http://localhost:3001/api/get")
        .then(response => response.json())
        .then(
            resData => {
                setResData(resData.data)
            }
        )
    }, [])

    console.log(resData)

    return (
        <div class = "main">
            <div className="sort">
                Sort By:
                <button>Popularity</button>
                <button>Rating</button>
                <button>Distance</button>
            </div>
            <div class = "restaurantList">
                <RestaurantCard />
                <RestaurantCard />
                <RestaurantCard />
                <RestaurantCard />
                <RestaurantCard />
                <RestaurantCard />
                <RestaurantCard />
                <RestaurantCard />
                <RestaurantCard />
                <RestaurantCard />
            </div>
        </div>

    )
}