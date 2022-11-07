import React, {useState, useEffect} from "react"
import RestaurantCard from "./RestaurantCard"


export default function ComponentTable() {

return (
    <div className="main">
        <div className="sort">
            Sort By:
            <button>Popularity</button>
            <button>Rating</button>
            <button>Distance</button>
        </div>
        <div className="restaurantList">
            {/* {resData.map((resData)=>

                <RestaurantCard props= {resData}/>
            )} */}
           {resData && <RestaurantCard props={resData[0]}/>}
        </div>
    </div>

)
