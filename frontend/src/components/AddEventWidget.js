const AddEventWidget = function (props) {
  const client = props.client;

  const [title, setTitle] = useState(props.title || "");
  const [location, setLocation] = useState(props.location || "");
  const [price, setPrice] = useState(props.price || "");

  const saveEvent = function () {
    let Event = {
      title: title,
      location: location,
      price: price,
    
    };

    client.action(window.schema, ["event", "create"], Event).then((result) => {
      props.eventSaved(result);
    });
  };

  return (
    <section>
      <label htmlFor="">Title</label>
      <input
        type="text"
        placeholder="Title"
        onChange={(event) => setTitle(event.target.value)}
        value={title}
      ></input>
      <label htmlFor="">Location</label>
      <select
        onChange={(event) => setLocation(event.target.value)}
        value={location}
      >
        {LOCATION_CHOICES.map((location, i) => (
          <option key={i} value={location.id}>
            {location.name}
          </option>
        ))}
      </select>

      <input
        type="number"
        placeholder="Ticket Price"
        onChange={(event) => setPrice(event.target.value)}
        value={price}
      ></input>
      <button type="button" onClick={() => saveEvent()}>
        Create Event
      </button>
    </section>
  );
};
