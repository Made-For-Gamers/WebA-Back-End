using AggAPIs.Models;
using Datalayer.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Middleware;

namespace AggAPIs.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ProjectsController : ControllerBase
    {
        private IProjectService _projectService;
        public ProjectsController(IProjectService projectService)
        {
            _projectService = projectService;
        }

        [HttpGet]
        [Authorize]
        public async Task<IEnumerable<Project>> GetProjects(
            [FromQuery] PaginationParams @params, 
            [FromQuery] ProjectsFiltering filter)
        {
            return await _projectService.GetProjects(
                    filter.GetFilter(),
                    @params.Page * @params.itemsPerPage, 
                    @params.ItemsPerPage
                    );


        }
    }
}
