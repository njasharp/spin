import streamlit as st

def create_spin_wheel_app():
    # Set page config
    st.set_page_config(
        page_title="Spin the Wheel!",
        page_icon="🎯",
        layout="wide"
    )
    
    # Add title and description
    st.title("🎯 Spin the Wheel!")
    st.write("Click the wheel to spin and win tickets!")

    # HTML and JavaScript code for the spinning wheel
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Spin the Wheel</title>
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
                {"label": "🎟️", "value": 1,  "question": "1 Ticket"},
                {"label": "🎟️", "value": 2,  "question": "2 Tickets"},
                {"label": "🎟️", "value": 3,  "question": "3 Tickets"},
                {"label": "🎟️", "value": 4,  "question": "4 Tickets"},
                {"label": "🎟️", "value": 5,  "question": "5 Tickets"},
                {"label": "🎟️", "value": 6,  "question": "6 Tickets"},
                {"label": "🎟️", "value": 7,  "question": "7 Tickets"},
                {"label": "🎟️", "value": 8,  "question": "8 Tickets"},
                {"label": "🎟️", "value": 9,  "question": "9 Tickets"},
                {"label": "🎟️", "value": 10, "question": "10 Tickets"}
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
                container.on("click", null);
                if(oldpick.length == data.length){
                    oldpick = [];
                }
                var ps = 360/data.length,
                    pieslice = Math.round(1440/data.length),
                    rng = Math.floor((Math.random() * 1440) + 360);
                rotation = (Math.round(rng / ps) * ps);
                picked = Math.round(data.length - (rotation % 360)/ps);
                picked = picked >= data.length ? (picked % data.length) : picked;
                if(oldpick.indexOf(picked) !== -1){
                    d3.select(this).call(spin);
                    return;
                } else {
                    oldpick.push(picked);
                }
                rotation += 90 - Math.round(ps/2);
                vis.transition()
                    .duration(3000)
                    .attrTween("transform", rotTween)
                    .each("end", function(){
                        d3.select("#question h1")
                            .text(data[picked].question);
                        oldrotation = rotation;
                        container.on("click", spin);
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
        </script>
    </body>
    </html>
    """

    # Embed the HTML code using st.components.v1.html
    st.components.v1.html(html_code, height=600)

    # Add instructions
    with st.expander("How to Play"):
        st.write("""
        1. Click the 'SPIN' button in the center of the wheel
        2. Wait for the wheel to stop spinning
        3. See how many tickets you've won!
        4. The wheel can be spun multiple times
        """)

if __name__ == "__main__":
    create_spin_wheel_app()