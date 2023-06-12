<script>
    let phone1 = "";
    let data = {};
    let showTablePage = false;
  
    const goBack = () => {
      showTablePage = false;
    };
  
    async function summary_of_total() {
      const formData = new FormData();
      formData.append("phone1", phone1);
  
      try {
        const res = await fetch("http://127.0.0.1:5000/summary_of_total", {
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
            <h1>SUMMARY TOTAL</h1>
            <div class="input-container text-center p-4">
                <form on:submit|preventDefault={summary_of_total}>
                    <label for="mobileNumber">Mobile No:</label>
                    <input class="me-4" id="mobileNumber"  type="text" placeholder="Enter Mobile No" size="10" bind:value={phone1}/>
                    <button class="btn" type="submit">Submit</button>
                </form>
            </div>
        </div>
    </div>
    {/if}

</center>
<style>
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
  