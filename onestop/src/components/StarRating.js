// export const $RatingStarButton = styled.div<RatingStarProps>`
//   width: 50px;
//   height: 50px;
//   display: inline-block;
//   cursor: pointer;
//   background-size: contain;
//   background-repeat: no-repeat;
//   background-position: center;

//   &:not(:last-child) {
//     margin-right: 15px;
//   }
//   background-image: ${(props) =>
//     props.active ? `URL(${activeStar})` : `URL(${inactiveStar})`};
// `;



// // for the render star method, pass in a value that == restaurant rating
// //iterate over 5 times to generate 5 stars. 
// // each star should have an index value. If the restaurant rating is greater than the index, 
// //    set the value of {active} to false. 
// //    when [active] is false, it will 


// [1,2,3,4,5].map((star, i) => {
//   return(
    
//     <$RatingStarButton active={restaurantRating > i} /> 
//   )
// })


// // [1,2,3,4,5].map((star, i) => {

// //   if (i > restaurantRating) 
// //     return  <StarRating  /> 
// //   else if (i < restaurantRating)
// //     return <InActiveStar /> 
 
// // )
// // })

// const renderStars = (restaurantRating ) => {
//   let stars = [];

//   for (let rating = 1; rating <= 5; rating++) {
//     const key = `rating_${rating}`;
//     stars.push(
//       <$RatingStarButton
//       // assign a number to each star -
//       // if the star is > the rating number, then it will be inactive
//         active={true || false}
//         key={`funnel-star-rating-${rating}`}
//       />
//     );
//   }

//   return stars;
// };



// const RestaurantRating = (props) => {
//   const restaurant = props

//   return (
//       <div>{renderstars()}</div>
//   )
// }
