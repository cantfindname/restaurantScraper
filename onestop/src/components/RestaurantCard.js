import React from "react"

export default function Card(props){
    const restaurant = props.props

    function calculateRatingCount(){
        const TATotalRatingCount = restaurant.five_star + restaurant.four_star + 
            restaurant.three_star+ restaurant.two_star + restaurant.one_star

        const TotalRatingCount = TATotalRatingCount + restaurant.yl_rating_count

        return TotalRatingCount
    }

    function calculateRating(totalCount) {

        const WeightedScore = restaurant.five_star * 5 +  restaurant.four_star * 4 + 
            restaurant.three_star * 3 + restaurant.two_star * 2 + 
            restaurant.one_star * 1 + restaurant.yl_five_star * 5 + 
            restaurant.yl_four_star * 4 + restaurant.yl_three_star * 3 + 
            restaurant.yl_two_star * 2 + restaurant.yl_one_star * 1      

        let rating = Math.round((WeightedScore/totalCount)*10)/10
        return rating
    }

    return (
        <div className="resCard">
            <div className="resName">{restaurant.name}</div>
            <div className="resRating">Overall Rating: {calculateRating(calculateRatingCount())}</div>
            <div className="resRatingCount">{calculateRatingCount()} ratings</div>
            <div className="resAddrerss">{restaurant.address}</div>
        </div>
    )
}

