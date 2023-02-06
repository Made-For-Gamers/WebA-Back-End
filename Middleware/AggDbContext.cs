using Datalayer.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Datalayer
{
    public class AggDbContext : DbContext
    {
        public DbSet<User> Users { get; set; }
        public DbSet<Project> Projects { get; set; }

        public AggDbContext(DbContextOptions<AggDbContext> options)
       : base(options)
        {
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {

            modelBuilder.Entity<Project>()
                .Property("Id");
            modelBuilder.Entity<Project>()
                .Property("UserId");


            modelBuilder.Entity<User>()
                .Property("Id");
            modelBuilder.Entity<User>()
                .Property("PasswordHash");
        }
    }
}
