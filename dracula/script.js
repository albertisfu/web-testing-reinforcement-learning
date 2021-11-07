var redraw

/* only do all this when document has finished loading (needed for RaphaelJS) */
window.onload = function() {

  var width = 800
  var height = 900

  var g = new Dracula.Graph()

  /* add a simple node */

  g.addNode("cherry")

  /* add a node with a customized label */
  g.addNode("1", { label: "Tomato"})


  /* add a node with a customized shape
     (the Raphael graph drawing implementation can draw this shape, please
     consult the RaphaelJS reference for details http://raphaeljs.com/) */
  var render = function(r, n) {
    var label = r.text(0, 30, n.label).attr({ opacity: 1 })
    var status = r.text(0, 3, n.status).attr({ opacity: 1, class:"node"+n.ide })
    //the Raphael set is obligatory, containing all you want to display
    var set = r.set()
      .push(
        r.rect(-30, -13, 60, 30)
          .attr({stroke: '#00bf30', 'stroke-width': 2, r: 9 })
      )
      .push(label, status)

    // make the label show only on hover
    set.click(
      function mouseIn() {
        //label.animate({ opacity: 1, 'fill-opacity': 1 }, 500),
        tippy('.node01', {
          content: 'My tooltip!',
        });
        console.log(n.id);
      },
      function mouseOut() {
        //label.animate({ opacity: 0 }, 300)
      }
    )
    
    return set
  }

  g.addNode('id35', {
    label: "http://localhost:8080/page_1",
    status: "200",
    ide:"01",
    /* filling the shape with a color makes it easier to be dragged */
    /* arguments: r = Raphael object, n : node object */
    render: render
  })


  /* connect nodes with edges */

  g.addEdge('1', 'cherry', { directed: true })
  g.addEdge('cherry', 'apple', { directed: true })
  g.addEdge('id35', '1', { directed: true })

  /* customize the colors of that edge */
  // TODO currently not implemented
  /* add an unknown node implicitly by adding an edge */
  //g.removeNode("1");

  /* layout the graph using the Spring layout implementation */
  var layouter = new Dracula.Layout.Spring(g)

  /* draw the graph using the RaphaelJS draw implementation */
  var renderer = new Dracula.Renderer.Raphael('#paper', g, width, height)

  redraw = function() {
    layouter.layout()
    renderer.draw()
  }
  hide = function(id) {
    g.nodes[id].hide()
  }
  show = function(id) {
    g.nodes[id].show()
  };
  redraw()
}

