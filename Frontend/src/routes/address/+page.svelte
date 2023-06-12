<script>
  let phone1 = true;
  let phone1Value = "";
  let phone2 = "";
  let data = {};
  let showTablePage = false;

  const goBack = () => {
    showTablePage = false;
  };

  async function single_address() {
    const formData = new FormData();
    formData.append("phone1", phone1Value);
    formData.append("phone2", phone2)

    try {
      const res = await fetch("http://127.0.0.1:5000/single_address", {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        data = await res.json();
        showTablePage = true;
      } else {
        console.error("Failed to submit form");
      }
    } catch (error) {
      console.error("Error submitting form", error);
    }
  }
</script>

<center>
{#if showTablePage}
<div class="bottom-section">
  <button on:click={goBack}>Back</button>
  <table>
      <thead>
          <tr>
          {#each data.headers as head}
              <th>
              {head}
              </th>
          {/each}
          </tr>
      </thead>
      <tbody>
          {#each data.data_dict as item}
          <tr>
              {#each data.headers as header}
              <td>{item[header]}</td>
              {/each}
          </tr>
          {/each}
      </tbody>
  </table>
  </div> 
  {:else}
  <div class="shadow p-2 mt-4 border-top">
      
      <div class="text-center mt-2">
          <h1>SINGLE ADDRESS</h1>
          <div class="input-container text-center p-4">
              <form on:submit|preventDefault={single_address}>
                  <label for="single_address">Enter No:</label>
                  {#if phone1 === true}
                    <input id="mobileNumber1" type="text" placeholder="Enter Mobile No" bind:value={phone1Value}/>
                    {:else}
                      <input id="mobileNumber2" type="text" placeholder="Enter Mobile No" bind:value={phone2}/>
                  {/if}

                  <button class="btn" type="submit">Submit</button>
              </form>
          </div>
      </div>
  </div>
  {/if}

</center>
<style>
  .text-center {
      border: 2px;
  }
  .bottom-section {
    height: 60vh;
    overflow: auto;
    align-items: center;
    margin-top: 10px;
  }
  table{
    border: 1px solid black;
    margin-top: 10px;
  }
  .btn {
    box-sizing: content-box;
  }
</style>
