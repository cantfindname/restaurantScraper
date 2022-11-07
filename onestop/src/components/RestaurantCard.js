import React from "react"

export default function Card(props){
    const restaurant = props.props
    return (
        <div className="resCard">
            <div className="resName">{restaurant.name}</div>
            <div className="resRating">4/5</div>
            <div className="resRatingCount">123 ratings</div>
            <div className="resAddrerss">{restaurant.address}</div>
        </div>
            )
        }

