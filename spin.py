import streamlit as st
import pandas as pd
from datetime import datetime

def initialize_session_state():
    if 'spins_left' not in st.session_state:
        st.session_state.spins_left = 3
    if 'current_tickets' not in st.session_state:
        st.session_state.current_tickets = 0
    if 'high_scores' not in st.session_state:
        st.session_state.high_scores = pd.DataFrame(
            columns=['Player', 'Score', 'Date']
        )
    if 'game_active' not in st.session_state:
        st.session_state.game_active = True

def submit_score():
    player_name = st.session_state.player_name
    if player_name.strip():
        new_score = pd.DataFrame({
            'Player': [player_name],
            'Score': [st.session_state.current_tickets],
            'Date': [datetime.now().strftime("%Y-%m-%d %H:%M")]
        })
        st.session_state.high_scores = pd.concat([st.session_state.high_scores, new_score], ignore_index=True)
        st.session_state.high_scores = st.session_state.high_scores.sort_values(by='Score', ascending=False).head(10)
        # Reset game
        st.session_state.spins_left = 3
        st.session_state.current_tickets = 0
        st.session_state.game_active = True
        st.rerun()

def create_spin_wheel_app():
    # Initialize session state
    initialize_session_state()
    
    # Set page config
    st.set_page_config(
        page_title="Spin the Wheel Game!",
        page_icon="🎯",
        layout="wide"
    )
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("🎯 Spin the Wheel Game!")
        st.write(f"Spins left: {st.session_state.spins_left} | Current Tickets: {st.session_state.current_tickets}")

        # HTML and JavaScript code for the spinning wheel
        html_code = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <script src="https://d3js.org/d3.v3.min.js" charset="utf-8"></script>
            <style>
                text {
                    font-family: Helvetica, Arial, sans-serif;
                    font-size: 19px;
                    pointer-events: none;
                }
                #chart {
                    position: relative;
                    width: 500px;
                    height: 500px;
                    margin: 0 auto;
                }
                #question {
                    text-align: center;
                    margin-top: 20px;
                }
                #question h1 {
                    font-size: 32px;
                    font-weight: bold;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                    margin: 0;
                    padding: 10px;
                }
            </style>
        </head>
        <body>
            <div id="chart"></div>
            <div id="question"><h1></h1></div>

            <script>
                var padding = {top:20, right:40, bottom:0, left:0},
                    w = 360 - padding.left - padding.right,
                    h = 360 - padding.top  - padding.bottom,
                    r = Math.min(w, h) / 2,
                    rotation = 0,
                    oldrotation = 0,
                    picked = 100000,
                    oldpick = [],
                    color = d3.scale.category20();

                var data = [
                    {"label": "10🎟️", "value": 10,  "question": "10 Ticket"},
                    {"label": "20🎟️", "value": 20,  "question": "20 Tickets"},
                    {"label": "30🎟️", "value": 30,  "question": "30 Tickets"},
                    {"label": "40🎟️", "value": 40,  "question": "40 Tickets"},
                    {"label": "50🎟️", "value": 50,  "question": "50 Tickets"},
                    {"label": "60🎟️", "value": 60,  "question": "60 Tickets"},
                    {"label": "70🎟️", "value": 70,  "question": "70 Tickets"},
                    {"label": "80🎟️", "value": 80,  "question": "80 Tickets"},
                    {"label": "90🎟️", "value": 90,  "question": "90 Tickets"},
                    {"label": "100🎟️", "value": 100, "question": "100 Tickets"}
                ];

                var svg = d3.select('#chart')
                    .append("svg")
                    .data([data])
                    .attr("width",  w + padding.left + padding.right)
                    .attr("height", h + padding.top + padding.bottom);

                var container = svg.append("g")
                    .attr("class", "chartholder")
                    .attr("transform", "translate(" + (w/2 + padding.left) + "," + (h/2 + padding.top) + ")");

                var vis = container.append("g");

                var pie = d3.layout.pie().sort(null).value(function(d){ return 1; });

                var arc = d3.svg.arc().outerRadius(r);

                var arcs = vis.selectAll("g.slice")
                    .data(pie)
                    .enter()
                    .append("g")
                    .attr("class", "slice");

                arcs.append("path")
                    .attr("fill", function(d, i){ return color(i); })
                    .attr("d", function(d){ return arc(d); });

                arcs.append("text").attr("transform", function(d){
                    d.innerRadius = 0;
                    d.outerRadius = r;
                    d.angle = (d.startAngle + d.endAngle) / 2;
                    return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")translate(" + (d.outerRadius - 10) + ")";
                })
                .attr("text-anchor", "end")
                .text(function(d, i){ return data[i].label; });

                container.on("click", spin);

                function spin(d){
                    if (window.parent.document.querySelector('[data-testid="stMarkdownContainer"]').textContent.includes("Spins left: 0")) {
                        return;
                    }
                    
                    container.on("click", null);
                    var ps = 360/data.length,
                        pieslice = Math.round(1440/data.length),
                        rng = Math.floor((Math.random() * 1440) + 360);
                    rotation = (Math.round(rng / ps) * ps);
                    picked = Math.round(data.length - (rotation % 360)/ps);
                    picked = picked >= data.length ? (picked % data.length) : picked;
                    rotation += 90 - Math.round(ps/2);
                    
                    vis.transition()
                        .duration(3000)
                        .attrTween("transform", rotTween)
                        .each("end", function(){
                            d3.select("#question h1")
                                .text(data[picked].question);
                            oldrotation = rotation;
                            container.on("click", spin);
                            
                            // Send message to Streamlit
                            window.parent.postMessage({
                                type: "spin_result",
                                value: data[picked].value
                            }, "*");
                        });
                }

                svg.append("g")
                    .attr("transform", "translate(" + (w + padding.left + padding.right) + "," + ((h/2)+padding.top) + ")")
                    .append("path")
                    .attr("d", "M-" + (r*.15) + ",0L0," + (r*.05) + "L0,-" + (r*.05) + "Z")
                    .style({"fill":"black"});

                container.append("circle")
                    .attr("cx", 0)
                    .attr("cy", 0)
                    .attr("r", 60)
                    .style({"fill":"white","cursor":"pointer"});

                container.append("text")
                    .attr("x", 0)
                    .attr("y", 15)
                    .attr("text-anchor", "middle")
                    .text("SPIN")
                    .style({"font-weight":"bold", "font-size":"30px"});

                function rotTween(to) {
                    var i = d3.interpolate(oldrotation % 360, rotation);
                    return function(t) { return "rotate(" + i(t) + ")"; };
                }

                // Listen for messages from Streamlit
                window.addEventListener("message", function(event) {
                    if (event.data.type === "update_spins") {
                        // Handle spin update
                    }
                });
            </script>
        </body>
        </html>
        """

        # Handle spin result
        components_kwargs = dict(height=600)
        if st.session_state.game_active:
            components_kwargs["html"] = html_code
        else:
            st.write("Game Over! Submit your score to play again.")
        
        st.components.v1.html(**components_kwargs)

    with col2:
        st.title("🏆 High Scores")
        
        # Display high scores table
        if not st.session_state.high_scores.empty:
            st.dataframe(
                st.session_state.high_scores,
                hide_index=True,
                use_container_width=True
            )
        else:
            st.write("No high scores yet!")
        
        # Submit score section
        if st.session_state.spins_left == 0 and st.session_state.game_active:
            st.markdown("### Submit Your Score")
            st.text_input("Enter your name:", key="player_name")
            st.button("Submit Score", on_click=submit_score, disabled=not st.session_state.get('player_name', '').strip())

    # Add instructions
    with st.sidebar.expander("How to Play"):
        st.write("""
        1. You have 3 spins per game
        2. Click the 'SPIN' button in the center of the wheel
        3. Collect as many tickets as possible
        4. After 3 spins, enter your name and submit your score
        5. Try to get on the leaderboard!
        """)
    st.sidebar.info("build by darryl")
    # Handle spin result from JavaScript
    if st.session_state.spins_left > 0 and st.session_state.game_active:
        current_value = st.query_params.get("spin_result", None)
        if current_value is not None:
            current_value = int(current_value)
            st.session_state.current_tickets += current_value
            st.session_state.spins_left -= 1
            if st.session_state.spins_left == 0:
                st.session_state.game_active = False
            st.query_params.clear()
            st.rerun()

if __name__ == "__main__":
    create_spin_wheel_app()
