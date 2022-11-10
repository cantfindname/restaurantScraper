import React, {useState, useEffect} from "react"
import RestaurantCard from "./RestaurantCard"

export default function MainContent(props) {
    var isEmpty = false 
    const [resData, setResData] = useState(null)

    const fetchResData = () => {
        fetch('http://localhost:3001/api/get')
        .then(response =>response.json())
        .then(resData => (
        setResData(resData)))
        .catch(err => console.log(err))
    }
    useEffect(() => fetchResData(), [])

    useEffect(() => {
        // if props.searchedRestaurants == [] (or check .empty?)
        // then you call fetchResData again
        
        console.log(props.searchedRestaurants)
        props.searchedRestaurants && setResData(props.searchedRestaurants)
    },[props.searchedRestaurants])
    

    if (props.searchedRestaurants !== undefined && props.searchedRestaurants !== null && props.searchedRestaurants.length === 0){
        isEmpty = true  
    }
    // useEffect (()=>{
    //     fetch('http://localhost:3001/api/get')
    //     .then(response => response.json())
    //     .then(resData => setResData(JSON.parse(resData)))
    // }, [])
    console.log(resData)
    console.log(isEmpty)

    if (isEmpty){

        return (
            <div className = "noResult">
                <div className = "primaryMsg">Sorry, there is no result for the keyword you searched for</div>
                <div className = "secondaryMsg">Please check the spelling or try more general terms</div>
            </div>
        )
    }
    else {

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


}